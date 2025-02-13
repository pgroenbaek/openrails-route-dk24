import os
import time
import requests
import pandas as pd

export_directory = "..\\BDK_OPENDATA\\"
base_url = "https://services1.arcgis.com/QcgJt0vVxSaqMKl7/arcgis/rest/services/"
query_urls = [
    "Adgangsveje_OD/FeatureServer/0/query",
    "Afsnitsmidter_OD/FeatureServer/0/query",
    "Basisspor_OD/FeatureServer/0/query",
    "BDK_matrikler_OD/FeatureServer/0/query",
    "Belysning_Visning/FeatureServer/0/query",
    "BI_BTR_RELEASEAFSNIT_OD/FeatureServer/0/query",
    "Broer_og_tunneller_OpenData/FeatureServer/0/query",
    "BTR_knuder_OD/FeatureServer/0/query",
    "BTR_SPORDATA_M_OD/FeatureServer/0/query",
    "Fikspunkter_OD/FeatureServer/0/query",
    "FOR_PERRONER_OD/FeatureServer/0/query",
    "GENNEMLOEB_SCREENING_OD/FeatureServer/0/query",
    "Hegn_OpenData/FeatureServer/0/query",
    "H%c3%b8jsp%c3%a6nding_krydsning/FeatureServer/0/query",
    "Hovedstraekninger_HE_OD/FeatureServer/0/query",
    "Kilometrering_OD/FeatureServer/0/query",
    "LAAGER_OD/FeatureServer/0/query",
    "Laesseramper_visning/FeatureServer/0/query",
    "Noedaabninger_offentlig/FeatureServer/0/query",
    "Faunahegn/FeatureServer/0/query",
    "FaunaPassager/FeatureServer/0/query",
    "PLATFORME_OD/FeatureServer/0/query",
    "Referencepunkter_OD/FeatureServer/0/query",
    "RFB_Projekteret_KM/FeatureServer/0/query",
    "Signaler_OD/FeatureServer/0/query",
    "SIK_AFSMRK__OD/FeatureServer/1/query",
    "Sikrede_Overkoersel_OD/FeatureServer/0/query",
    "Sporforloeb_OD/FeatureServer/0/query",
    "Sporskifter_OD/FeatureServer/0/query",
    "Sporstoppere_OD/FeatureServer/0/query",
    "Stoejskaerme_Opendata/FeatureServer/0/query",
    "Stoettekonstruktioner_Opendata/FeatureServer/0/query",
    "Usikrede_overkoersler_OD/FeatureServer/0/query",
    "NyBaneVestfyn/FeatureServer/0/query"
]


if __name__ == "__main__":
    if not os.path.exists(export_directory): 
        os.makedirs(export_directory)

    for query_url in query_urls:
        layer_url = base_url + query_url
        params = {
            "where": "1=1",
            "outFields": "*",
            "f": "json",
            "resultOffset": 0,
            "resultRecordCount": 1000
        }

        all_features = []

        while True:
            response = requests.get(layer_url, params=params)
            data = response.json()
            
            if "features" not in data or len(data["features"]) == 0:
                break

            all_features.extend(data["features"])
            params["resultOffset"] += params["resultRecordCount"]
            time.sleep(10)

        csv_filename = export_directory + query_url.split("/")[0] + ".csv"
        df = pd.json_normalize(all_features)
        df.to_csv(csv_filename, index=False)

        print("Query %d of %d completed. Saved as %s" % (query_urls.index(query_url) + 1, len(query_urls), csv_filename))