from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

data = [
  {
    "type": "hospital",
    "name": "Sterling Hospital Vadodara",
    "url": "https://en.wikipedia.org/wiki/Sterling_Hospitals"
  },
  {
    "type": "hospital",
    "name": "Bhailal Amin General Hospital",
    "url": "https://www.baghospital.com/blog/cardiovascular-diseases-cvds"
  },
  {
    "type": "hospital",
    "name": "Sunshine Global Hospitals",
    "url": "https://www.sunshineglobalhospitals.com/about-us"
  },
  {
    "type": "hospital",
    "name": "Apollo Hospitals",
    "url": "https://en.wikipedia.org/wiki/Apollo_Hospitals"
  },
  {
    "type": "hospital",
    "name": "Care Hospitals",
    "url": "https://en.wikipedia.org/wiki/CARE_Hospitals"
  },
  {
    "type": "college",
    "name": "Parul University",
    "url": "https://en.wikipedia.org/wiki/Parul_University"
  },
  {
    "type": "college",
    "name": "Maharaja Sayajirao University of Baroda",
    "url": "https://en.wikipedia.org/wiki/Maharaja_Sayajirao_University_of_Baroda"
  },
  {
    "type": "college",
    "name": "Navrachana University",
    "url": "https://en.wikipedia.org/wiki/Navrachana_University"
  },
  {
    "type": "college",
    "name": "ITM Universe (Gwalior)",
    "url": "https://en.wikipedia.org/wiki/ITM_University_(Gwalior)"
  },
  {
    "type": "sports_club",
    "name": "Baroda Cricket Association",
    "url": "https://en.wikipedia.org/wiki/Baroda_Cricket_Association"
  },
  {
    "type": "sports_club",
    "name": "Lakshya Sports Club",
    "url": "https://lakshyasports.com/"
  },
  {
    "type": "Fitness Club",
    "name": "Health Club",
    "url": "https://en.wikipedia.org/wiki/Health_club"
  },
  {
    "type": "sports_club",
    "name": "MPC Gymkhana",
    "url": "https://historyofvadodara.in/polo-club-the-maharaja-pratapsinh-coronation-gymkhana/"
  },
  {
    "type": "sports_club",
    "name": "Gaekwad Baroda Golf Club",
    "url": "https://en.wikipedia.org/wiki/Samarjitsinh_Gaekwad"
  },
  {
    "type": "fruit_vegetable",
    "name": "Bigbasket - Vadodara",
    "url": "https://en.wikipedia.org/wiki/BigBasket"
  },
  {
    "type": "fruit_vegetable",
    "name": "FreshDirect - Vadodara",
    "url": "https://en.wikipedia.org/wiki/FreshDirect"
  },
  {
    "type": "fruit_vegetable",
    "name": "Reliance Fresh",
    "url": "https://en.wikipedia.org/wiki/Reliance_Retail"
  },
  {
    "type": "fruit_vegetable",
    "name": "Nature's Basket",
    "url": "https://en.wikipedia.org/wiki/Nature%27s_Basket"
  },
  {
    "type": "fruit_vegetable",
    "name": "VegEase",
    "url": "https://krishijagran.com/agriculture-apps/vegease/"
  },
  {
    "type": "movie",
    "name": "INOX - Vadodara",
    "url": "https://en.wikipedia.org/wiki/PVR_INOX#INOX_Leisure"
  },
  {
    "type": "movie",
    "name": "Cinepolis - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Cin%C3%A9polis"
  },
  {
    "type": "movie",
    "name": "PVR Cinemas - Vadodara",
    "url": "https://fr.wikipedia.org/wiki/PVR_Cinemas"
  },
  {
    "type": "movie",
    "name": "Miraj Cinemas - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Miraj_Cinemas"
  },
  {
    "type": "movie",
    "name": "Cinemarc - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Cinemark_Theatres"
  },
  {
    "type": "famous_place",
    "name": "Laxmi Vilas Palace",
    "url": "https://en.wikipedia.org/wiki/Lakshmi_Vilas_Palace,_Vadodara"
  },
  {
    "type": "famous_place",
    "name": "Sayaji Baug",
    "url": "https://en.wikipedia.org/wiki/Sayaji_Baug"
  },
  {
    "type": "famous_place",
    "name": "EME Temple",
    "url": "https://en.wikipedia.org/wiki/EME_Temple"
  },
  {
    "type": "famous_place",
    "name": "Baroda Museum and Picture Gallery",
    "url": "https://en.wikipedia.org/wiki/Baroda_Museum_%26_Picture_Gallery"
  },
  {
    "type": "famous_place",
    "name": "Kirti Mandir",
    "url": "https://en.wikipedia.org/wiki/Kirti_Mandir,_Vadodara"
  },
  {
    "type": "restaurant",
    "name": "Mandap - Express Hotel",
    "url": "https://expresshotelsindia.com/hotel-express-budget-hotel-in-vadodara/"
  },
  {
    "type": "restaurant",
    "name": "Fiorella - The Fern Residency",
    "url": "https://www.fernhotels.com/about-us"
  },
  {
    "type": "restaurant",
    "name": "22nd Parallel",
    "url": "https://22ndparallel.com/about-us/"
  },
  {
    "type": "restaurant",
    "name": "Peshawri - WelcomHotel",
    "url": "https://www.itchotels.com/in/en/welcomhotelvadodara"
  },
  {
    "type": "restaurant",
    "name": "The Gateway Hotel - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Gateway_Hotel"
  },
  {
    "type": "gym",
    "name": "Gold's Gym - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Gold%27s_Gym"
  },
  {
    "type": "gym",
    "name": "Talwalkars Gym - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Talwalkars"
  },
  {
    "type": "gym",
    "name": "Anytime Fitness - Vadodara",
    "url": "hhttps://en.wikipedia.org/wiki/Anytime_Fitness"
  },
  {
    "type": "gym",
    "name": "Cross Garage",
    "url": "https://en.wikipedia.org/wiki/CrossFit"
  },
  {
    "type": "bank",
    "name": "Bank of Baroda",
    "url": "https://en.wikipedia.org/wiki/Bank_of_Baroda"
  },
  {
    "type": "bank",
    "name": "State Bank of India - Vadodara",
    "url": "https://en.wikipedia.org/wiki/State_Bank_of_India"
  },
  {
    "type": "bank",
    "name": "ICICI Bank - Vadodara",
    "url": "https://en.wikipedia.org/wiki/ICICI_Bank"
  },
  {
    "type": "bank",
    "name": "HDFC Bank - Vadodara",
    "url": "https://en.wikipedia.org/wiki/HDFC_Bank"
  },
  {
    "type": "bank",
    "name": "Axis Bank - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Axis_Bank"
  },
  {
    "type": "supermarket",
    "name": "Big Bazaar - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Smart_Bazaar"
  },
  {
    "type": "supermarket",
    "name": "D-Mart - Vadodara",
    "url": "https://en.wikipedia.org/wiki/DMart"
  },
  {
    "type": "supermarket",
    "name": "Reliance Fresh - Vadodara",
    "url": "https://relianceretail.com/reliance-fresh.html"
  },
  {
    "type": "supermarket",
    "name": "Spencer's - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Spencer%27s_Retail"
  },
  {
    "type": "supermarket",
    "name": "More Megastore - Vadodara",
    "url": "https://en.wikipedia.org/wiki/More_(store)"
  },
  {
    "type": "gas_company",
    "name": "Adani Gas - Vadodara",
    "url": "https://www.adanigas.com/"
  },
  {
    "type": "gas_company",
    "name": "Gujarat Gas - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Gujarat_Gas"
  },
  {
    "type": "gas_company",
    "name": "Indian Oil Corporation - Vadodara Refinery",
    "url": "https://en.wikipedia.org/wiki/Indian_Oil_Corporation"
  },
  {
    "type": "jail",
    "name": "Vadodara Central Jail",
    "url": "https://historyofvadodara.in/central-jail/"
  },
  {
    "type": "transport_service",
    "name": "Vadodara Municipal Transport Service",
    "url": "https://en.wikipedia.org/wiki/Gujarat_State_Road_Transport_Corporation"
  },
  {
    "type": "others",
    "name": "Vadodara Municipal Corporation",
    "url": "https://en.wikipedia.org/wiki/Vadodara_Municipal_Corporation"
  },
  {
    "type": "others",
    "name": "Vadodara Chamber of Commerce and Industry",
    "url": "https://en.wikipedia.org/wiki/Gujarat_Chamber_of_Commerce_%26_Industry"
  },
  {
    "type": "airport",
    "name": "Vadodara Airport",
    "url": "https://en.wikipedia.org/wiki/Vadodara_Airport"
  },
  {
    "type": "restaurant",
    "name": "Mainland China - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Mainland_China"
  },
  {
    "type": "restaurant",
    "name": "Little Italy - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Little_Italy"
  },
  {
    "type": "restaurant",
    "name": "Barbeque Nation - Vadodara",
    "url": "https://www.barbequenation.com/about-us"
  },
  {
    "type": "restaurant",
    "name": "Canara Coffee House",
    "url": "https://en.wikipedia.org/wiki/Canara_Coffee_House"
  },
  {
    "type": "restaurant",
    "name": "Sur Sagar - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Sursagar_Lake"
  },
  {
    "type": "gym",
    "name": "Fitness Culture",
    "url": "https://en.wikipedia.org/wiki/Fitness_culture"
  },
  {
    "type": "gym",
    "name": "Anytime Fitness - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Anytime_Fitness"
  },
  {
    "type": "gym",
    "name": "Gym Shark",
    "url": "https://en.wikipedia.org/wiki/Gymshark"
  },
  {
    "type": "gym",
    "name": "Indian Club",
    "url": "https://en.wikipedia.org/wiki/Indian_club"
  },
  {
    "type": "gym",
    "name": "Fit World - Vadodara",
    "url": "https://en.wikipedia.org/wiki/World_Fit"
  },
  {
    "type": "bank",
    "name": "IDBI Bank - Vadodara",
    "url": "https://en.wikipedia.org/wiki/IDBI_Bank"
  },
  {
    "type": "bank",
    "name": "Kotak Mahindra Bank - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Kotak_Mahindra_Bank"
  },
  {
    "type": "bank",
    "name": "Central Bank of India - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Central_Bank_of_India"
  },
  {
    "type": "bank",
    "name": "Punjab National Bank - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Punjab_National_Bank"
  },
  {
    "type": "bank",
    "name": "Bank of India - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Bank_of_India"
  },
  {
    "type": "supermarket",
    "name": "Spencer's - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Spencer%27s_(department_store)"
  },
  {
    "type": "supermarket",
    "name": "Reliance Market",
    "url": "https://relianceretail.com/reliance-market.html"
  },
  {
    "type": "supermarket",
    "name": "Star Bazaar - Vadodara",
    "url": "https://www.indianretailer.com/article/whats-hot/policy/Star-Bazaar-becomes-a-bone-of-contention.a81"
  },
  {
    "type": "supermarket",
    "name": "Heritage Fresh - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Heritage_Foods"
  },
  {
    "type": "supermarket",
    "name": "Sahakari Bhandar - Vadodara",
    "url": "https://www.sahakaribhandar.com/about-us.html"
  },
  {
    "type": "gas_company",
    "name": "GSPC Gas - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Gujarat_State_Petroleum_Corporation"
  },
  {
    "type": "gas_company",
    "name": "GAIL Gas - Vadodara",
    "url": "https://en.wikipedia.org/wiki/GAIL"
  },
  {
    "type": "gas_company",
    "name": "Torrent Gas - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Torrent_Group"
  },
  {
    "type": "gas_company",
    "name": "Indraprastha Gas - Vadodara",
    "url": "https://en.wikipedia.org/wiki/Indraprastha_Gas"
  },
  {
    "type": "jail",
    "name": "Mumbai Central Jail",
    "url": "https://en.wikipedia.org/wiki/Mumbai_Central_Jail"
  },
  {
    "type": "jail",
    "name": "Sabarmati Central Jail",
    "url": "https://en.wikipedia.org/wiki/Sabarmati_Central_Jail"
  },
  {
    "type": "transport_service",
    "name": "Vadodara Bus Service",
    "url": "https://en.wikipedia.org/wiki/Vadodara_bus_station"
  },
  {
    "type": "transport_service",
    "name": "Gujarat Metro Rail Corporation",
    "url": "https://en.wikipedia.org/wiki/Gujarat_Metro_Rail_Corporation_Limited"
  },
  {
    "type": "others",
    "name": "Vadodara Municipal Corporation",
    "url": "https://www.wikiwand.com/en/Vadodara_Municipal_Corporation"
  },
  {
    "type": "others",
    "name": "Vadodara Chamber of Commerce and Industry",
    "url": "https://www.vccivadodara.org/about_detail"
  },
  {
    "type": "others",
    "name": "Vadodara Stock Exchange",
    "url": "https://en.wikipedia.org/wiki/Vadodara_Stock_Exchange"
  },
  {
    "type": "others",
    "name": "Vadodara Central Library",
    "url": "https://www.baroda.com/2/Sightseeing-In-Vadodara/Baroda-Central-Library"
  }
]

df = pd.DataFrame(data)

def filter_urls_by_type(df, type_to_search):
    filtered_df = df[df['type'] == type_to_search]
    return filtered_df

def scrape_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ')
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def get_similarity_scores(df):
    df['content'] = df['url'].apply(scrape_content)
    documents = df['content'].tolist()
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    cosine_similarities = cosine_similarity(tfidf_matrix)
    return df, cosine_similarities

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['GET'])
def search():
    user_input_type = request.args.get('query').strip().lower()
    filtered_df = filter_urls_by_type(df, user_input_type)
    if filtered_df.empty:
        return f"No URLs found for the type: {user_input_type}", 404

    results_df, similarity_scores = get_similarity_scores(filtered_df)
    avg_similarity_scores = similarity_scores.mean(axis=1)
    results_df['avg_similarity_score'] = avg_similarity_scores
    sorted_results = results_df.sort_values(by='avg_similarity_score', ascending=False)
    
    return render_template('results.html', results=sorted_results.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)
