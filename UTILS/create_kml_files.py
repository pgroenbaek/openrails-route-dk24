"""
Copyright (C) 2025 Peter Grønbæk Andersen <peter@grnbk.io>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import json
import simplekml
import pandas as pd
from pyproj import Proj, Transformer


TRANSFORMER = Transformer.from_crs("EPSG:25832", "EPSG:4326", always_xy=True)
OUTPUT_PATH = "../ROUTES/OR_DK24"


def create_stations_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df = pd.read_csv("../DATA/Afsnitsmidter_OD.csv")
    df_stations = df[df["attributes.AFSNITSTYPE"].isin(["Station", "Trinbræt"])]
    df_stations.apply(lambda row: kml.newpoint(
        name="%s (%s)" % (row["attributes.NAVN"], row["attributes.FORKORTELSE"]),
        coords=[(row["attributes.WGS_X"],row["attributes.WGS_Y"])]
    ), axis=1)
    kml.save(OUTPUT_PATH + "/denmark-stations.kml")


def create_signals_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df = pd.read_csv("../DATA/Signaler_OD.csv")
    df["attributes.WGS_X"], df["attributes.WGS_Y"] = zip(*df.apply(lambda row: TRANSFORMER.transform(
        row["geometry.x"], row["geometry.y"]
    ), axis=1))
    df.apply(lambda row: kml.newpoint(
        name="%s" % row["attributes.TYPE"] +
            ('' if pd.isna(row["attributes.NUMMER"]) else " %s" % row["attributes.NUMMER"]) +
            ('' if pd.isna(row["attributes.NAVN"]) else " %s" % row["attributes.NAVN"]),
        coords=[(row["attributes.WGS_X"], row["attributes.WGS_Y"])]
    ), axis=1)
    kml.save(OUTPUT_PATH + "/denmark-signals.kml")


def create_mileposts_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df = pd.read_csv("../DATA/Kilometrering_OD.csv")
    df["attributes.WGS_X"], df["attributes.WGS_Y"] = zip(*df.apply(lambda row: TRANSFORMER.transform(
        row["geometry.x"], row["geometry.y"]
    ), axis=1))
    df.apply(lambda row: kml.newpoint(
        name=("Km %0.1f" % row["attributes.KM"]).replace(".", ","),
        coords=[(row["attributes.WGS_X"], row["attributes.WGS_Y"])]
    ), axis=1)
    kml.save(OUTPUT_PATH + "/denmark-mileposts.kml")


def create_markers_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df = pd.read_csv("../DATA/SIK_AFSMRK__OD.csv")
    df["attributes.WGS_X"], df["attributes.WGS_Y"] = zip(*df.apply(lambda row: TRANSFORMER.transform(
        row["geometry.x"], row["geometry.y"]
    ), axis=1))
    df.apply(lambda row: kml.newpoint(
        name=str(row["attributes.DESCRIPT"]),
        coords=[(row["attributes.WGS_X"], row["attributes.WGS_Y"])]
    ), axis=1)
    kml.save(OUTPUT_PATH + "/denmark-markers.kml")


def create_trackelevation_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df_fixpunkter = pd.read_csv("../DATA/Fikspunkter_OD.csv")
    df_fixpunkter = df_fixpunkter[df_fixpunkter["attributes.Z"] != 0.0]
    df_fixpunkter["attributes.WGS_X"], df_fixpunkter["attributes.WGS_Y"] = zip(*df_fixpunkter.apply(lambda row: TRANSFORMER.transform(
        row["geometry.x"], row["geometry.y"]
    ), axis=1))
    df_fixpunkter.apply(lambda row: kml.newpoint(
        name=(("%0.1f m" % row["attributes.Z"]).replace(".", ",")),
        coords=[(row["attributes.WGS_X"], row["attributes.WGS_Y"])]
    ), axis=1)
    df_refpunkter = pd.read_csv("../DATA/Referencepunkter_OD.csv")
    df_refpunkter = df_refpunkter[df_refpunkter["attributes.Z"] != 0.0]
    df_refpunkter["attributes.WGS_X"], df_refpunkter["attributes.WGS_Y"] = zip(*df_refpunkter.apply(lambda row: TRANSFORMER.transform(
        row["geometry.x"], row["geometry.y"]
    ), axis=1))
    df_refpunkter.apply(lambda row: kml.newpoint(
        name=(("%0.1f m" % row["attributes.Z"]).replace(".", ",")),
        coords=[(row["attributes.WGS_X"], row["attributes.WGS_Y"], row["attributes.Z"])]
    ), axis=1)
    kml.save(OUTPUT_PATH + "/denmark-trackelevation.kml")


def create_bridgestunnels_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df = pd.read_csv("../DATA/Broer_og_tunneller_OpenData.csv")
    mapping = {
        1: "Vejbærende bro",
        2: "Sporbærende bro",
        3: "Stibærende bro",
        4: "Rørgennemløb (Spv < 2 m)",
        6: "Ledningstunnel",
        10: "Højbro over farvande",
        20: "Dalbro",
        30: "Pæledæk",
        40: "Tunnel",
        81: "Rørbygværk (OF af rørledning)",
        97: "Andet",
        98: "Ukendt"
    }
    df["attributes.label"] = df["attributes.bygart"].map(mapping)
    df["attributes.WGS_X"], df["attributes.WGS_Y"] = zip(*df.apply(lambda row: TRANSFORMER.transform(
        row["geometry.x"], row["geometry.y"]
    ), axis=1))
    df.apply(lambda row: kml.newpoint(
        name=str(row["attributes.label"]),
        coords=[(row["attributes.WGS_X"], row["attributes.WGS_Y"], 30)]
    ), axis=1)
    kml.save(OUTPUT_PATH + "/denmark-bridgestunnels.kml")


def create_noisewalls_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df = pd.read_csv("../DATA/Stoejskaerme_Opendata.csv")
    df.apply(lambda row: [
        kml.newlinestring(
            name=str(row["attributes.STOEJSKAER"]),
            coords=[TRANSFORMER.transform(x, y) for x, y in path]
        ) for path in json.loads(row["geometry.paths"])
    ], axis=1)
    kml.save(OUTPUT_PATH + "/denmark-noisewalls.kml")


def create_supportstructures_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df = pd.read_csv("../DATA/Stoettekonstruktioner_Opendata.csv")
    df.apply(lambda row: [
        kml.newlinestring(
            name=str(row["attributes.bygbetegn"]),
            coords=[[x, y] for x, y in path]
        ) for path in json.loads(row["geometry.paths"])
    ], axis=1)
    kml.save(OUTPUT_PATH + "/denmark-supportstructures.kml")


def create_fences_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df = pd.read_csv("../DATA/Hegn_Opendata.csv")
    df.apply(lambda row: [
        kml.newlinestring(
            name=str(row["attributes.HEGN_TYPE"]).replace("4", ""),
            coords=[TRANSFORMER.transform(x, y) for x, y in path]
        ) for path in json.loads(row["geometry.paths"])
    ], axis=1)
    kml.save(OUTPUT_PATH + "/denmark-fences.kml")


def create_nybanevestfyn_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df = pd.read_csv("../DATA/NyBaneVestfyn.csv")
    [kml.newlinestring(
        name="Hsp 1",
        coords=[TRANSFORMER.transform(x, y) for x, y in path]
    ) for path in json.loads(df.iloc[192327]["geometry.paths"])]
    [kml.newlinestring(
        name="Hsp 2",
        coords=[TRANSFORMER.transform(x, y) for x, y in path]
    ) for path in json.loads(df.iloc[192328]["geometry.paths"])]
    [kml.newlinestring(
        name="Hsp 1",
        coords=[TRANSFORMER.transform(x, y) for x, y in path]
    ) for path in json.loads(df.iloc[159516]["geometry.paths"])]
    [kml.newlinestring(
        name="Hsp 2",
        coords=[TRANSFORMER.transform(x, y) for x, y in path]
    ) for path in json.loads(df.iloc[159517]["geometry.paths"])]

    # TODO configure ranges of terrain/fences properly
    df.iloc[24480:27480].apply(lambda row: [
        kml.newpoint(
            name="Terrain",
            coords=[TRANSFORMER.transform(path[0][0], path[0][1])]
        ) for path in json.loads(row["geometry.paths"])
    ], axis=1)
    df.iloc[30752:33120].apply(lambda row: [
        kml.newpoint(
            name="Terrain",
            coords=[TRANSFORMER.transform(path[0][0], path[0][1])]
        ) for path in json.loads(row["geometry.paths"])
    ], axis=1)
    df.iloc[85132:86443].apply(lambda row: [
        kml.newpoint(
            name="Terrain",
            coords=[TRANSFORMER.transform(path[0][0], path[0][1])]
        ) for path in json.loads(row["geometry.paths"])
    ], axis=1)
    df.iloc[86816:88019].apply(lambda row: [
        kml.newpoint(
            name="Terrain",
            coords=[TRANSFORMER.transform(path[0][0], path[0][1])]
        ) for path in json.loads(row["geometry.paths"])
    ], axis=1)
    kml.save(OUTPUT_PATH + "/nybanevestfyn.kml")


def create_levelcrossings_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df_sikret = pd.read_csv("../DATA/Sikrede_Overkoersel_OD.csv")
    df_sikret["attributes.WGS_X"], df_sikret["attributes.WGS_Y"] = zip(*df_sikret.apply(lambda row: TRANSFORMER.transform(
        row["geometry.x"], row["geometry.y"]
    ), axis=1))
    df_sikret.apply(lambda row: kml.newpoint(
        name=(("Ovk %s - %s (Sikret)" % (row["attributes.OVKNR"], row["attributes.KATEGORI"]))),
        coords=[(row["attributes.WGS_X"], row["attributes.WGS_Y"])]
    ), axis=1)
    df_usikret = pd.read_csv("../DATA/Usikrede_overkoersler_OD.csv")
    df_usikret["attributes.WGS_X"], df_usikret["attributes.WGS_Y"] = zip(*df_usikret.apply(lambda row: TRANSFORMER.transform(
        row["geometry.x"], row["geometry.y"]
    ), axis=1))
    df_usikret.apply(lambda row: kml.newpoint(
        name=(("Ovk %s - %s (Usikret)" % (row["attributes.OVKNR"], row["attributes.TYPE"]))),
        coords=[(row["attributes.WGS_X"], row["attributes.WGS_Y"])]
    ), axis=1)
    kml.save(OUTPUT_PATH + "/denmark-levelcrossings.kml")


def create_powerlines_kml(OUTPUT_PATH):
    kml = simplekml.Kml()
    df = pd.read_csv("../DATA/H%c3%b8jsp%c3%a6nding_krydsning.csv")
    df["attributes.WGS_X"], df["attributes.WGS_Y"] = zip(*df.apply(lambda row: TRANSFORMER.transform(
        row["geometry.x"], row["geometry.y"]
    ), axis=1))
    df.apply(lambda row: kml.newpoint(
        name=(("%s %s" % (row["attributes.SPAENDING"], row["attributes.SPORNUMMER"]))),
        coords=[(row["attributes.WGS_X"], row["attributes.WGS_Y"])]
    ), axis=1)
    kml.save(OUTPUT_PATH + "/denmark-powerlines.kml")


if __name__ == "__main__":
    create_stations_kml(OUTPUT_PATH)
    create_signals_kml(OUTPUT_PATH)
    create_mileposts_kml(OUTPUT_PATH)
    create_markers_kml(OUTPUT_PATH)
    create_trackelevation_kml(OUTPUT_PATH)
    create_bridgestunnels_kml(OUTPUT_PATH)
    create_noisewalls_kml(OUTPUT_PATH)
    create_supportstructures_kml(OUTPUT_PATH)
    create_fences_kml(OUTPUT_PATH)
    create_nybanevestfyn_kml(OUTPUT_PATH)
    create_levelcrossings_kml(OUTPUT_PATH)
    create_powerlines_kml(OUTPUT_PATH)
