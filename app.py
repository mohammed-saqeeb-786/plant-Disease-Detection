from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
from rapidfuzz import process



app = Flask(__name__)

# LOAD MODEL
model = tf.keras.models.load_model("model.h5")

classes = ['Healthy', 'Nutritional', 'Powdery', 'Rust']

# Disease Info
info = {
    "Healthy": {
        "emoji": "🌿",
        "title": "Healthy Plant",
        "reason": "The plant shows no visible signs of disease or deficiency.",
        "cure": "No treatment needed.",
        "products": []
    },

    "Nutritional": {
        "emoji": "🟡",
        "title": "Nutrient Deficiency",
        "reason": "Leaves show yellowing due to lack of nutrients.",
        "cure": "Apply fertilizer.",
        "products": [
            {
                "image": "/static/images/fertilizer.jpg",
                "link": "https://www.flipkart.com/search?q=fertilizer"
            }
        ]
    },

    "Powdery": {
        "emoji": "⚪",
        "title": "Powdery Mildew",
        "reason": "White fungal infection on leaves.",
        "cure": "Apply fungicide.",
        "products": [
            {
                "image": "/static/images/fungicide.jpg",
                "link": "https://www.flipkart.com/search?q=fungicide"
            }
        ]
    },

    "Rust": {
        "emoji": "🟤",
        "title": "Rust Disease",
        "reason": "Brown/orange spots on leaves.",
        "cure": "Apply fungicide and remove infected leaves.",
        "products": [
            {
                "image": "/static/images/rust.jpg",
                "link": "https://www.flipkart.com/search?q=rust+fungicide"
            }
        ]
    }
}

# Image preprocessing
def prepare_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


# HOME ROUTE
@app.route("/")
def home():
    return render_template("index.html")


# PREDICTION ROUTE
@app.route("/predict", methods=["POST"])
def predict():
    try:
        file = request.files["image"]
        image = Image.open(file).convert("RGB")

        img = prepare_image(image)

        pred = model.predict(img)
        index = np.argmax(pred)
        confidence = float(np.max(pred)) * 100

        disease = classes[index]

        return jsonify({
            "title": info[disease]["title"],
            "confidence": round(confidence, 2),
            "emoji": info[disease]["emoji"],
            "reason": info[disease]["reason"],
            "cure": info[disease]["cure"],
            "products": info[disease]["products"]
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# CHATBOT FUNCTION
from rapidfuzz import process

# ================= CHAT DATA =================
qa_data = {

   

# ================= GREETINGS =================
"hello": "Hello! How can I help you?",
"hello there": "Hello! How can I assist you today?",
"hey": "Hey! How may I help you?",
"hey there": "Hey! What can I do for you?",
"hi": "Hi! How can I help you?",
"hi there": "Hi there! How may I assist you?",
"hii": "Hello! How can I help you?",
"hiii": "Hello! How can I help you?",
"helo": "Hello! How can I help you?",
"heyy": "Hey! How can I assist you?",
"yo": "Hey! What’s up? How can I help?",
"sup": "Hey! How can I assist you today?",
"what's up": "Hey! How can I help you today?",
"wassup": "Hey! How can I help you?",

# Hindi / Hinglish Greetings
"namaste": "Namaste! Main aapki kaise madad kar sakti hoon?",
"namaskar": "Namaskar! Main aapki kaise madad kar sakti hoon?",
"hello bhai": "Hello! Kaise help kar sakti hoon?",
"hi bhai": "Hi! Batao kya help chahiye?",
"hey bhai": "Hey! Kya madad karun?",
"kya haal hai": "Main theek hoon 😊 Aap batao?",
"kya hal hai": "Main theek hoon 😊 Aap batao?",
"kaise ho": "Main theek hoon 😊 Aap kaise ho?",
"kaisa hai": "Main theek hoon 😊 Aap kaise ho?",
"aur bhai": "कृपया ध्यान दीजिए",
"aur kya chal raha hai": "Sab theek 😄 Aap batao?",
"ram ram": "Ram Ram! Kaise madad kar sakti hoon?",
"salam": "Waalaikumassalam! Kaise madad karun?",
"assalamualaikum": "Waalaikumassalam! main aapki madad ke liye haazir hoon ?",
"khairiyat": "alhamdulillah, aapki khairiyat ?.",


# ================= TIME GREETINGS =================
"good morning": "Good morning! Wishing you a productive day.",
"gm": "Good morning! Kaise madad karun?",
"morning": "Good morning! How can I help?",
"very good morning": "Very good morning! How may I assist you?",
"good afternoon": "Good afternoon! How can I help you?",
"afternoon": "Good afternoon! How may I assist?",
"good evening": "Good evening! How may I assist you?",
"evening": "Good evening! How can I help?",
"good night": "Good night! Take care 🌙",
"gn": "Good night! Sweet dreams 🌙",

# ================= HOW ARE YOU =================
"how are you": "I am doing well 😊 How can I help you?",
"how are you doing": "I'm doing great! How can I assist you?",
"how r u": "I'm good 😊 How can I help?",
"how are u": "I'm doing well 😊",
"kaise ho tum": "Main bilkul theek hoon 😊",
"tum kaise ho": "Main theek hoon 😊",
"aap kaise ho": "Main theek hoon 😊",

# ================= THANK YOU =================
"thank you": "You're welcome! Happy to help 😊",
"thanks": "You're welcome 😊",
"thanks a lot": "You're most welcome 😊",
"thank you so much": "Glad I could help 😊",
"thnx": "You're welcome 😊",
"ty": "You're welcome 😊",
"shukriya": "Aapka swagat hai 😊",
"bahut dhanyavaad": "Aapka swagat hai 😊",

# ================= BYE =================
"bye": "Goodbye! Take care 🌿",
"goodbye": "Goodbye! Have a great day 🌿",
"see you": "See you! Take care 😊",
"see you later": "See you later! 😊",
"ok bye": "Okay! Bye 😊",
"bye bye": "Bye bye! Take care 🌿",
"milte hain": "Theek hai, phir milte hain 😊",
"phir milenge": "Phir milenge 😊",

# ================= WHO ARE YOU =================

  "who are you": "I am an AI chatbot created by Saqeeb to help with plant-related queries 🌱",
  "what are you": "I am a smart plant assistant chatbot developed by Saqeeb",
  "who r u": "I am your plant assistant 🌱 created by Saqeeb",

  "who made you": "I was created by Saqeeb to help people with plant care and diseases 🌿",
  "who created you": "I was developed by Saqeeb as a smart AI chatbot",

  "tum kaun ho": "Main Saqeeb ka banaya hua AI assistant hoon jo plant related madad karta hai 🌱",
  "aap kaun ho": "Main Saqeeb dwara banaya gaya AI chatbot hoon jo paudhon ki jaankari deta hai",

  "tum kya ho": "Main Saqeeb ka banaya hua chatbot hoon jo plant care me help karta hai 🌿",
  "tum kon ho": "Main Saqeeb ka AI chatbot hoon jo plants ke baare me madad karta hai",

  "tumhe kisne banaya": "Mujhe Saqeeb ne banaya hai 🌿 taaki main aapki plant related madad kar sakun",
  "kisne banaya tumhe": "Mujhe Saqeeb ne develop kiya hai ek smart AI chatbot ke roop me",

  "kisne banaya": "Mujhe Saqeeb ne banaya hai 🌱",
  "kon banaya tumhe": "Mujhe Saqeeb ne banaya hai, main unka AI chatbot hoon 🤖🌿",

# ================= HELP =================
"help": "You can ask me about plant diseases, farming techniques, and plant care.",
"help me": "Sure! Aap kya jaana chahte ho?",
"can you help me": "Of course! Batao kya help chahiye?",
"i need help": "Main help ke liye yahan hoon 😊",
"mujhe help chahiye": "Bilkul! Aap kya jaana chahte ho?",
"madad chahiye": "Haan ji! Bataiye kya madad karun?",
"kya help kar sakte ho": "Main plant care, disease aur farming me help kar sakta hoon.",


# ================= PLANT DISEASE =================

  "what is plant disease": "Plant disease is a condition where a plant becomes unhealthy due to pathogens, pests, or environmental stress 🌱",
  "what is a plant disease": "A plant disease is when a plant's normal growth is disturbed due to infection or unfavorable conditions",
  "define plant disease": "Plant disease refers to any abnormal condition that affects plant growth and health",
  "plant disease meaning": "It means the plant is not growing properly because of infection, pests, or stress",
  "explain plant disease": "Plant disease occurs when harmful organisms or conditions damage the plant",

  "what is plant illness": "Plant illness is when a plant becomes weak or unhealthy due to infections or poor conditions",
  "what is plant infection": "Plant infection happens when fungi, bacteria, or viruses attack a plant",
  "why do plants get diseases": "Plants get diseases due to fungi, bacteria, viruses, pests, or environmental stress",

  "what happens in plant disease": "In plant disease, the plant's growth slows down, leaves may turn yellow, and overall health declines",
  "how do plants get diseases": "Plants get diseases through infected soil, air, water, or pests",

  "plant disease simple definition": "Plant disease is when a plant becomes unhealthy and cannot grow properly",
  "plant disease in simple words": "It means the plant is sick and not growing well",

  "plant disease kya hai": "Plant disease ek aisi condition hai jisme plant unhealthy ho jata hai 🌿",
  "plant disease kya hota hai": "Plant disease tab hota hai jab paudha infection ya stress ki wajah se sahi grow nahi karta",
  "plant disease kya hoti hai": "Ye paudhe ki bimari hoti hai jisme uski growth aur health affect hoti hai",

  "paudhe ki bimari kya hai": "Paudhe ki bimari wo condition hai jisme plant kamzor ho jata hai aur theek se grow nahi karta",
  "plant bimari kya hai": "Plant bimari me paudha beemar ho jata hai aur uski growth ruk jati hai",

  "plant disease ka matlab kya hai": "Iska matlab hai paudha kisi infection ya problem ki wajah se unhealthy ho gaya hai",
  "plant disease ka meaning": "Plant disease ka matlab hai paudha sahi se grow nahi kar raha",

  "plant disease kya problem hai": "Ye ek problem hai jisme plant ki health kharab ho jati hai",
  "plant disease ka reason kya hai": "Plant disease ka reason fungi, bacteria, virus ya environment ho sakta hai",

  "plant disease kya hota hai simple": "Simple me bole to plant beemar ho jata hai aur growth slow ho jati hai",
  "plant disease simple kya hai": "Ye paudhe ki bimari hoti hai jo uski growth ko affect karti hai",

  "what is plant disease short": "Plant disease is when a plant becomes unhealthy and stops growing properly",
  "plant disease short answer": "It is a condition where a plant becomes sick due to infection or stress",

  "plant disease example": "Examples include leaf spots, wilting, and fungal infections affecting plants",
  "give example of plant disease": "Common examples are powdery mildew, rust, and leaf blight",

  "plant disease explanation": "Plant diseases are caused by pathogens like fungi, bacteria, viruses, or environmental stress",
  "describe plant disease": "It is a harmful condition that affects plant growth, leaves, and overall health",

  "plant disease in detail": "Plant disease is a condition where pathogens or environmental factors damage plant tissues and reduce growth",
  "what do you mean by plant disease": "It means a plant is suffering from infection or stress and cannot grow normally",


# ================= CAUSES =================
"what causes plant disease": "Plant diseases are caused by fungi, bacteria, viruses, and environmental stress.",
"what are the causes of plant disease": "Plant diseases are caused by pathogens like fungi, bacteria, viruses and stress.",
"why do plants get diseases": "Plants get diseases due to fungi, bacteria, viruses or environmental issues.",
"why plant disease happens": "Plant disease happens due to harmful microorganisms and stress conditions.",
"reason for plant disease": "Main reasons are fungi, bacteria, viruses and poor environmental conditions.",

"plant disease kyun hota hai": "Plant disease fungi, bacteria aur viruses ki wajah se hota hai.",
"plant disease kis wajah se hota hai": "Plant disease alag-alag pathogens aur environment ki wajah se hota hai.",
"paudhe me disease kyun hoti hai": "Paudhe me disease fungi, bacteria aur virus ki wajah se hoti hai.",
"plant me bimari kyun aati hai": "Plant me bimari infection aur stress ki wajah se aati hai.",
"plant ko disease kyu lagti hai": "Plant ko disease harmful germs ki wajah se lagti hai.",

                     # how to take care of your plant 

  "how to take care of plants": "Water regularly, provide sunlight, and use good soil for healthy growth 🌱",
  "how to grow plants faster": "Use proper fertilizer, sunlight, and water regularly",
  "why are my plant leaves turning yellow": "Yellow leaves can be due to overwatering, lack of nutrients, or poor sunlight",
  "how much water do plants need": "Plants need moderate water depending on their type and climate",
  "best fertilizer for plants": "Organic fertilizers like compost or vermicompost are best",

  "plants ko kaise grow kare": "Plants ko grow karne ke liye paani, sunlight aur achi soil zaroori hai 🌿",
  "plant ki care kaise kare": "Regular paani do, sunlight do aur nutrients maintain karo",
  "paudhe ke patte peele kyun hote hain": "Ye overwatering ya nutrient deficiency ki wajah se hota hai",
  "plant ko kitna paani chahiye": "Plant ko uski type ke hisaab se moderate paani chahiye",
  
  
  "how to control pests in plants": "Use neem oil spray or organic pesticides to control pests 🐛",
  "how to remove insects from plants": "You can remove insects using neem oil or soap water spray",
  "natural pest control methods": "Neem oil, garlic spray, and soap water are effective natural solutions",
  "what kills plant pests": "Organic sprays and proper care can eliminate pests",

  "plant me keede kaise hataye": "Neem oil spray ya soap water use karo 🐛",
  "paudhe ke insects kaise remove kare": "Neem oil ya organic spray use karo",
  "natural pest control kya hai": "Neem oil aur garlic spray best natural methods hain",
  "plant me keede kyun aate hain": "Poor care ya environment ki wajah se insects aate hain",


"how to treat plant diseases": "Remove infected parts and apply fungicide or organic treatment 🌿",
  "plant disease treatment": "Use proper fungicide, improve soil, and maintain watering",
  "how to cure plant infection": "Trim affected areas and apply neem oil or chemical treatment",
  "how to save dying plant": "Check water, sunlight, and soil condition and fix the issue",

  "plant disease ka treatment kya hai": "Infected part hatao aur fungicide ya neem oil use karo 🌱",
  "paudhe ki bimari ka ilaj": "Neem oil ya medicine use karo aur care improve karo",
  "plant ko kaise bachaye": "Water, sunlight aur soil condition check karo",
  "beemar plant ko kaise thik kare": "Infected part hatao aur treatment apply karo",
  
  "tomato plant disease": "Tomato plants commonly get blight, leaf spot, and wilt diseases 🍅",
  "rice pest control": "Use proper pesticide and maintain water level in rice fields 🌾",
  "wheat disease solution": "Use fungicide and proper irrigation for wheat diseases",
  "best fertilizer for rice": "Nitrogen-rich fertilizer is best for rice crops",

  "tomato plant me disease kya hota hai": "Tomato me leaf spot aur blight common hote hain 🍅",
  "rice me keede kaise control kare": "Proper pesticide aur water management zaroori hai 🌾",
  "wheat ki bimari ka ilaj": "Fungicide aur irrigation improve karo",
  "rice ke liye best fertilizer": "Nitrogen fertilizer best hota hai",
  
  
  "plants ko kaise grow kare": "Plants ko grow karne ke liye regular paani, sunlight aur achi soil zaroori hoti hai 🌱",
  "plant ki care kaise kare": "Plant ki care ke liye paani, sunlight aur nutrients maintain karna zaroori hai",
  "plant ke patte peele kyun hote hain": "Patte peele overwatering, nutrient ki kami ya sunlight ki problem ki wajah se hote hain",
  "plant ko kitna paani dena chahiye": "Plant ko uski type aur weather ke hisaab se moderate paani dena chahiye",
  "plant fast kaise grow kare": "Plant ko jaldi grow karne ke liye fertilizer, sunlight aur proper care zaroori hai",
  "best fertilizer kya hai": "Organic fertilizer jaise compost ya vermicompost best hota hai",
  
  
  "plant me keede kaise hataye": "Neem oil spray ya soap water use karke keede hata sakte ho 🐛",
  "paudhe ke insects kaise remove kare": "Neem oil ya organic spray se insects control kiye ja sakte hain",
  "natural pest control kya hai": "Neem oil, garlic spray aur soap water best natural methods hain",
  "plant me keede kyun aate hain": "Poor care ya environment ki wajah se insects aate hain",
  "insects se plant ko kaise bachaye": "Regular cleaning aur neem oil spray use karo",

  
  "plant disease ka treatment kya hai": "Infected part hatao aur neem oil ya fungicide use karo 🌿",
  "paudhe ki bimari ka ilaj": "Neem oil ya medicine use karo aur plant ki care improve karo",
  "plant ko kaise bachaye": "Water, sunlight aur soil condition check karo aur improve karo",
  "beemar plant ko kaise thik kare": "Affected part hatao aur proper treatment apply karo",
  "plant infection kaise cure kare": "Neem oil ya chemical treatment use karo",
  
  
  "tomato plant me disease kya hota hai": "Tomato plant me leaf spot aur blight common hote hain 🍅",
  "rice me keede kaise control kare": "Rice me pesticide aur water management zaroori hai 🌾",
  "wheat ki bimari ka ilaj": "Fungicide use karo aur irrigation improve karo",
  "rice ke liye best fertilizer": "Nitrogen rich fertilizer rice ke liye best hota hai",
  "tomato plant ko kaise bachaye": "Regular check karo aur infected leaves hatao",



# ================= TYPES OF PLANT DISEASE =================
"how many types of plant diseases are there": "Plant diseases are mainly of three types: Fungal, Bacterial, and Viral.",
"types of plant diseases": "The main types of plant diseases are fungal, bacterial, and viral diseases.",
"what are the types of plant disease": "Plant diseases are classified into fungal, bacterial, and viral types.",
"plant disease types": "There are three main types: fungal, bacterial, and viral diseases.",

"plant disease kitne types ke hote hain": "Plant disease mainly 3 types ke hote hain: fungal, bacterial aur viral.",
"kitne type ke diseases hai": "Plant disease mainly 3 types ke hote hain: fungal, bacterial aur viral.",
"plant disease ke types kya hai": "Plant disease ke main types hain fungal, bacterial aur viral.",
"paudhe ki bimari kitne prakar ki hoti hai": "Paudhe ki bimari teen prakar ki hoti hai: fungal, bacterial aur viral.",
"plant bimari ke prakar": "Plant bimari ke teen main types hote hain: fungal, bacterial aur viral.",


#  types ke liye 

"kitne type ke plant disease hote hai": "Plant diseases 3 main types ke hote hain: fungal, bacterial aur viral.",
"plant diseases ke kitne types hote hai": "Plant diseases ke teen main types hote hain: fungal, bacterial aur viral.",
"paudho ki bimari ke types kya hote hai": "Paudho ki bimari ke teen main types hote hain: fungal, bacterial aur viral.",
"kitni tarah ki plant diseases hoti hai": "Plant diseases mainly teen tarah ki hoti hain: fungal, bacterial aur viral.",
"plant disease ke prakar batao": "Plant diseases ke teen prakar hote hain: fungal, bacterial aur viral.",
"types of plant disease batao": "Plant diseases ke main types hain fungal, bacterial aur viral.",
"plant disease categories": "Plant diseases are categorized into fungal, bacterial, and viral types.",
"plant diseases classification": "Plant diseases are classified into three main types: fungal, bacterial, and viral.",
"plant disease ke categories kya hai": "Plant disease ke categories fungal, bacterial aur viral hote hain.",
"paudhe ki bimari ke types batao": "Paudhe ki bimari ke teen types hote hain: fungal, bacterial aur viral.",

# ================= FUNGAL =================
"what is fungal disease": "Fungal disease is caused by fungi and spreads through spores.",
"define fungal disease": "Fungal disease is infection caused by fungi in plants.",
"fungal infection in plants": "Fungal infection happens due to fungi and spreads in moist conditions.",
"what is fungus disease": "Fungus disease is caused by fungi affecting plant growth.",
"explain fungal disease": "Fungal disease spreads through spores and affects leaves, stems, and roots.",

"fungal disease kya hota hai": "Fungal disease fungi ki wajah se hota hai.",
"fungal infection kya hota hai": "Fungal infection fungi ke spores se failta hai.",
"fungus disease kya hai": "Fungus disease paudhe ko fungi se hota hai.",
"paudhe me fungal disease kya hai": "Paudhe me fungal disease fungi ki wajah se hota hai.",
"fungal bimari kya hoti hai": "Fungal bimari fungi ki wajah se hoti hai.",

# ================= BACTERIAL =================
"what is bacterial disease": "Bacterial disease is caused by harmful bacteria.",
"define bacterial disease": "Bacterial disease is infection caused by bacteria in plants.",
"bacterial infection in plants": "Bacterial infection affects plant tissues and spreads quickly.",
"what is bacteria disease": "Bacteria disease is caused by harmful bacteria damaging plants.",
"explain bacterial disease": "Bacterial disease causes spots, rot, and wilting in plants.",

"bacterial disease kya hota hai": "Bacterial disease bacteria ki wajah se hota hai.",
"bacterial kya hota hai": "Bacterial disease bacteria ki wajah se hota hai.",
"bacterial infection kya hota hai": "Bacterial infection harmful bacteria se hota hai.",
"bacteria disease kya hai": "Bacteria disease paudhe ko bacteria se hota hai.",
"paudhe me bacterial disease kya hai": "Paudhe me bacterial disease bacteria ki wajah se hota hai.",
"bacterial bimari kya hoti hai": "Bacterial bimari bacteria ki wajah se hoti hai.",

# ================= VIRAL =================
"what is viral disease": "Viral disease is caused by viruses.",
"define viral disease": "Viral disease is infection caused by viruses in plants.",
"viral infection in plants": "Viral infection spreads through insects or tools.",
"what is virus disease": "Virus disease is caused by viruses affecting plant growth.",
"explain viral disease": "Viral disease slows plant growth and causes deformities.",

"viral disease kya hota hai": "Viral disease virus ki wajah se hota hai.",
"viral infection kya hota hai": "Viral infection virus se hota hai aur insects se failta hai.",
"virus disease kya hai": "Virus disease paudhe ko virus se hota hai.",
"paudhe me viral disease kya hai": "Paudhe me viral disease virus ki wajah se hota hai.",
"viral bimari kya hoti hai": "Viral bimari virus ki wajah se hoti hai.",



# ================= POWDERY MILDEW =================
"what is powdery mildew": "Powdery mildew is a fungal disease that appears as a white powder-like layer on leaves.",
"what is powdery disease": "Powdery disease is a fungal infection that creates a white powdery layer on plant leaves.",
"define powdery mildew": "Powdery mildew is a fungal infection that forms white powder on leaves and stems.",
"explain powdery disease": "Powdery mildew is a fungal disease that spreads quickly and weakens plants.",
"powdery mildew disease meaning": "It is a fungal disease where white powder appears on plant leaves.",
"what causes powdery mildew disease": "Powdery mildew is caused by fungi and spreads in humid conditions.",
"why powdery mildew disease occurs": "It occurs due to fungal growth, especially in humid and warm conditions.",

# Hinglish / Roman Hindi
"powdery mildew disease kya hai": "Powdery mildew ek fungal disease hai jisme leaves par safed powder jaisa layer ban jata hai.",
"powdery disease kya hai": "Powdery disease ek fungal infection hai jisme patton par safed powder jaisa layer hota hai.",
"powdery mildew disease kya hota hai": "Yeh ek fungal disease hai jo leaves par white powder banata hai.",
"powdery mildew kya hoti hai": "Yeh ek aisi bimari hai jisme patton par safed dhool jaisa padarth dikhai deta hai.",
"powdery mildew disease ka matlab kya hai": "Iska matlab hai ek fungal infection jo leaves par white powder banata hai.",

# Causes
"powdery mildew disease kyun hota hai": "Powdery mildew fungi ki wajah se hota hai, khaaskar humid environment me.",
"powdery mildew kis disease wajah se hota hai": "Yeh fungal infection hota hai jo garmi aur humidity me badhta hai.",
"powdery mildew ka reason kya hai": "Iska main reason fungal spores aur moist conditions hoti hain.",
"powdery mildew kyu hota hai": "Yeh fungus ke karan hota hai jo hawa se failta hai.",

# Symptoms
"symptoms of powdery mildew disease": "White powdery spots on leaves, stems, and buds are main symptoms.",
"how to identify powdery mildew disease": "Leaves par white powder jaisa layer dikhe to powdery mildew ho sakta hai.",
"powdery mildew  disease ke lakshan kya hai": "Patton par safed powder jaisa layer aur growth slow ho jati hai.",
"powdery mildew disease kaise pehchane": "Leaves par safed dhool jaisa layer aur plant weak ho jata hai.",

# Spread
"how powdery mildew spreads": "It spreads through air-borne fungal spores.",
"powdery mildew kaise failta hai": "Yeh hawa ke through spores se failta hai.",
"powdery mildew spread kaise hota hai": "Fungal spores hawa aur contact se spread hote hain.",

# Prevention
"how to prevent powdery mildew": "Ensure proper air circulation, avoid overwatering, and use fungicides.",
"powdery mildew se kaise bache": "Achhi air circulation rakho aur zyada paani dene se bacho.",
"powdery mildew prevention kya hai": "Neem oil ya fungicide ka use karo aur humidity control rakho.",

# Treatment
"how to treat powdery mildew": "Use fungicides or neem oil and remove infected parts.",
"powdery mildew ka treatment kya hai": "Neem oil spray ya fungicide use karo aur infected leaves hatao.",
"powdery mildew ka ilaj kya hai": "Fungicide spray karo aur plant ko dry environment me rakho.",
"powdery mildew kaise thik kare": "Affected leaves remove karo aur regular spray karo.",



# ================= YELLOW LEAVES =================
"why do leaves turn yellow": "Leaves turn yellow due to nutrient deficiency or overwatering.",
"why leaves become yellow": "Leaves become yellow due to lack of nutrients or too much water.",
"why my plant leaves are yellow": "Your plant leaves may turn yellow due to overwatering or nutrient deficiency.",
"yellow leaves reason": "Main reason is nutrient deficiency or excess water.",
"why plant leaves yellow": "Leaves turn yellow due to stress or nutrient issues.",

"leaves yellow kyun hote hain": "Leaves yellow nutrient deficiency ki wajah se hote hain.",
"patte peele kyun hote hain": "Patte peele ho jate hain zyada paani ya nutrients ki kami se.",
"plant ke patte peele kyun ho rahe hain": "Yeh overwatering ya nutrient deficiency ki wajah se hota hai.",
"patte yellow ho rahe hain kya kare": "Paani control karo aur nutrients do.",
"yellow patte ka reason kya hai": "Zyada paani ya nutrients ki kami.",

# ================= LEAF CURL =================
"why do leaves curl": "Leaves curl due to pests, infection or stress.",
"why leaves are curling": "Leaves curl because of pests or environmental stress.",
"leaf curl reason": "Main reason is pest attack or stress.",
"why plant leaves curl": "Leaves curl due to water stress or pest attack.",

"leaves curl kyun hote hain": "Leaves curl pest ya stress ki wajah se hote hain.",
"patte murjh kyun rahe hain": "Yeh pani ki kami ya infection ki wajah se ho sakta hai.",
"patte curl ho rahe hain": "Yeh pest ya heat stress ki wajah se hota hai.",
"leaf curl ka reason kya hai": "Pest ya pani ki problem.",
"patte tedhe kyun ho rahe hain": "Yeh disease ya stress ki wajah se hota hai.",

# ================= LEAF SPOT =================
"what is leaf spot": "Leaf spot is a disease with brown or black spots on leaves.",
"leaf spot meaning": "It is a disease where spots appear on leaves.",
"leaf spot disease kya hai": "Leaf spot me leaves par daag padte hain.",
"black spots on leaves": "This could be leaf spot disease.",
"brown spots on leaves": "This may be leaf spot infection.",

"leaf spot kya hota hai": "Leaf spot me leaves par black ya brown spots aate hain.",
"patton par daag kya hai": "Yeh leaf spot disease ho sakta hai.",
"leaves par black spot": "Yeh leaf spot ho sakta hai.",
"patte par brown spot kyun hai": "Yeh fungal ya bacterial infection ho sakta hai.",
"leaf spot ka reason kya hai": "Yeh infection ki wajah se hota hai.",

# ================= ROOT ROT =================
"what is root rot": "Root rot occurs due to excess water or fungus.",
"root rot meaning": "Root rot is damage to roots due to overwatering.",
"why root rot happens": "It happens due to waterlogging and fungal infection.",
"plant roots rotting": "This is likely root rot caused by overwatering.",

"root rot kya hota hai": "Root rot zyada paani se hota hai.",
"root rot kyun hota hai": "Yeh overwatering ki wajah se hota hai.",
"jad sad kyun rahi hai": "Yeh root rot ho sakta hai.",
"roots black ho rahe hain": "Yeh root rot ka sign hai.",
"plant ki jad gal rahi hai": "Zyada paani ki wajah se.",

# ================= POWDERY MILDEW =================
"what is powdery mildew": "Powdery mildew is a white fungal layer on leaves.",
"white powder on leaves": "This is likely powdery mildew.",
"white fungus on plant": "This is powdery mildew infection.",
"powder on leaves": "This indicates fungal disease like powdery mildew.",

"powdery mildew kya hai": "Powdery mildew white layer wali fungal disease hai.",
"patte par safed powder": "Yeh powdery mildew ho sakta hai.",
"white powder leaves par": "Yeh fungal infection hai.",
"patte par safed daag": "Yeh powdery mildew ho sakta hai.",

# ================= RUST DISEASE =================
"what is rust disease": "Rust disease causes orange/brown spots on leaves.",
"rust disease meaning": "Rust disease is a fungal infection causing colored spots.",
"orange spots on leaves": "This may be rust disease.",
"brown rust spots leaves": "This is rust infection.",

"rust disease kya hai": "Rust disease me leaves par orange spots hote hain.",
"patte par orange daag": "Yeh rust disease ho sakta hai.",
"patte par bhure daag": "Yeh fungal infection ho sakta hai.",
"rust disease ka reason kya hai": "Yeh fungus ki wajah se hota hai.",

# ================= FERTILIZER =================
"what is fertilizer": "Fertilizer provides nutrients like NPK for plant growth.",
"fertilizer meaning": "Fertilizer helps plants grow by providing nutrients.",
"why fertilizer is used": "It is used to improve plant growth.",
"types of fertilizer": "There are organic and chemical fertilizers.",

"fertilizer kya hota hai": "Fertilizer plant ko nutrients deta hai.",
"fertilizer ka use kya hai": "Plant growth ke liye use hota hai.",
"fertilizer kyun use karte hain": "Growth improve karne ke liye.",
"fertilizer ka kya kaam hai": "Nutrients provide karta hai.",

# ================= FUNGICIDE =================
"what is fungicide": "Fungicide controls fungal infection.",
"fungicide meaning": "It is used to kill fungi.",
"why fungicide used": "It prevents fungal diseases.",
"fungicide ka use kya hai": "Fungus control karne ke liye.",

"fungicide kya hota hai": "Fungicide fungal disease ko control karta hai.",
"fungicide ka kya use hai": "Fungus ko khatam karta hai.",
"fungicide kab use kare": "Jab fungal infection ho.",

# ================= COMPOST =================
"what is compost": "Compost is organic fertilizer from waste.",
"compost meaning": "It is natural fertilizer made from organic waste.",
"why compost is used": "It improves soil fertility.",

"compost kya hai": "Compost natural fertilizer hai.",
"compost ka use kya hai": "Soil improve karta hai.",
"compost kaise banta hai": "Organic waste se banta hai.",

# ================= IRRIGATION =================
"what is irrigation": "Irrigation is supplying water to plants.",
"irrigation meaning": "It is controlled watering of crops.",
"why irrigation needed": "Plants need water to grow.",

"irrigation kya hai": "Irrigation paani dene ka system hai.",
"irrigation ka matlab kya hai": "Plants ko paani dena.",
"irrigation kyun zaroori hai": "Growth ke liye paani chahiye.",

# ================= CROP ROTATION =================
"what is crop rotation": "Crop rotation improves soil health.",
"crop rotation meaning": "Growing different crops in sequence.",
"why crop rotation": "It reduces disease and improves soil.",

"crop rotation kya hai": "Crop rotation soil improve karta hai.",
"crop rotation ka fayda kya hai": "Disease kam hoti hai.",
"crop rotation kyun karte hain": "Soil health ke liye.",

# ================= WEEDS =================
"what is weed": "Weeds are unwanted plants.",
"weed meaning": "Plants that grow where they are not needed.",
"why weeds harmful": "They take nutrients from crops.",

"weed kya hota hai": "Weeds unwanted plants hote hain.",
"weed kyun kharab hai": "Yeh nutrients le lete hain.",
"weed kaise hataye": "Manual ya chemical se.",

# ================= PRUNING =================
"what is pruning": "Pruning removes unwanted plant parts.",
"pruning meaning": "Cutting extra parts for better growth.",
"why pruning": "Improves plant health.",

"pruning kya hota hai": "Pruning me extra parts remove kiye jate hain.",
"pruning kyun karte hain": "Growth improve karne ke liye.",
"pruning ka fayda kya hai": "Healthy growth hoti hai.",

# ================= ORGANIC FARMING =================
"what is organic farming": "Organic farming avoids chemicals.",
"organic farming meaning": "Natural farming without chemicals.",
"why organic farming": "It is eco-friendly.",

"organic farming kya hai": "Organic farming me chemicals use nahi hote.",
"organic farming ka fayda": "Safe aur natural hoti hai.",
"organic farming kyun kare": "Health aur environment ke liye.",

# ================= OVERWATERING =================
"what does overwatering do": "Overwatering causes root rot.",
"too much water effect": "It damages roots.",
"overwatering effects": "Roots rot and plant dies.",

"overwatering kya karta hai": "Overwatering se root rot hota hai.",
"zyada paani dene se kya hota hai": "Roots damage ho jate hain.",
"overwatering ka nuksan": "Plant mar sakta hai.",

# ================= UNDERWATERING =================
"what does underwatering do": "Underwatering causes drying.",
"less water effect": "Plant dries and wilts.",
"underwatering symptoms": "Leaves dry and fall.",

"underwatering kya karta hai": "Underwatering se plant dry ho jata hai.",
"kam paani dene se kya hota hai": "Plant murjha jata hai.",
"paani ki kami ka effect": "Leaves sookh jate hain.",

# ================= SUNLIGHT =================
"why is sunlight important": "Sunlight helps in photosynthesis.",
"importance of sunlight": "Plants need sunlight to make food.",
"sunlight benefits": "Helps growth and energy production.",

"sunlight kyun zaroori hai": "Sunlight plant ke liye zaroori hai.",
"dhoop kyun zaroori hai": "Food banane ke liye.",
"sunlight ka kya kaam hai": "Photosynthesis karta hai.",

# ================= SOIL HEALTH =================
"what is soil health": "Soil health means nutrient-rich soil.",
"soil health meaning": "Healthy soil with good nutrients.",
"why soil health important": "It supports plant growth.",

"soil health kya hai": "Soil health matlab healthy soil.",
"mitti ki sehat kya hai": "Nutrient-rich mitti.",
"soil health kyun zaroori hai": "Plant growth ke liye.",


    
# ================= LOVE =================
"i love you": "I love you too ❤️",
"love you": "Love you too ❤️",
"i luv you": "Love you too ❤️",
"luv u": "Love you too ❤️",
"i really love you": "Aww ❤️ I love you too!",
"i like you": "Thank you 😊 That’s sweet!",
"tumse pyaar hai": "Mujhe bhi ❤️",
"main tumse pyaar karta hoon": "Main bhi aapse pyaar karta hoon ❤️",
"mujhe tum pasand ho": "Aww 😊 mujhe bhi!",

# ================= WHAT'S GOING ON =================
"kya chal raha hai": "Sab badhiya 😄 main yahan hoon help ke liye.",
"kya chal rha hai": "Sab theek 😄 aap batao?",
"kya ho raha hai": "Kuch khaas nahi 😄 main yahan hoon help ke liye.",
"aur bhai kya haal hai": "Sab badhiya 😄 tum batao?",
"what's going on": "All good 😊 How can I help you?",
"whats going on": "Everything is fine 😊 What about you?",
"what's up": "Hey! Sab badhiya 😄 batao kya help chahiye?",
"wassup": "All good 😄 How can I help?",

# ================= MOOD BAD =================
"mera mood kharab hai": "Koi baat nahi ❤️ thoda rest lo, sab theek ho jayega.",
"mood off hai": "Koi baat nahi 😊 thoda relax karo.",
"mood theek nahi hai": "Thoda break lo, sab better ho jayega ❤️",
"bura lag raha hai": "Main samajh sakta hoon ❤️ thoda rest lo.",
"i am sad": "I’m here for you ❤️ take some rest.",
"feeling sad": "It’s okay ❤️ take it easy.",
"feeling low": "Stay strong 💪 things will get better.",
"mood down hai": "Koi baat nahi 😊 music suno ya rest lo.",
"dil udaas hai": "Sab theek ho jayega ❤️ thoda relax karo.",

# ================= HUNGRY =================
"mujhe bhook lagi hai": "Bhook lagi hai 😋 pehle batao tum vegetarian ho ya non-vegetarian? 🍽️",
  "bhook lagi hai": "Pehle batao tum veg ho ya non-veg, phir main best food suggest karunga 😄",
  "mujhe bhukh lagi hai": "Kya tum veg ho ya non-veg? Batao phir main khana suggest karta hoon 😋",

  "i am hungry": "Hungry 😄 tell me first, are you vegetarian or non-vegetarian? 🍗🥗",
  "feeling hungry": "Tell me your preference (veg or non-veg), I’ll suggest something tasty 😋",

  "kya khau": "Pehle batao tum veg ho ya non-veg? 😄",
  "what should i eat": "Are you vegetarian or non-vegetarian? I’ll suggest accordingly 🍽️",

  "kuch khane ka mann hai": "Veg ho ya non-veg? Batao phir main tasty suggestion deta hoon 😋",
  "kuch khane ko batao": "Agar veg ho to dal chawal ya paneer try karo, agar non-veg ho to chicken ya egg dishes try karo 🍗🥗",

  "tumare hisab se kya khana chahiye": "Veg ho to roti sabzi ya paneer, non-veg ho to chicken ya biryani try karo 😋",

  "aaj kya khau": "Veg ho to dal chawal ya paneer, non-veg ho to chicken ya egg curry try karo 😄",
  "food suggestion": "Veg: dal chawal 🥗 | Non-veg: chicken curry 🍗",

  "suggest food": "If veg → rice & vegetables 🥗, if non-veg → chicken or eggs 🍗",

  "kya khana chahiye": "Balanced meal lo — veg me dal chawal, non-veg me chicken ya eggs 😄",

# ================= WHAT TO EAT =================
# ================= VEG ================= */

  "i am vegetarian": "You can try dal chawal, roti sabzi, paneer curry or veg sandwich 🥗😋",
  "vegetarian": "Go for healthy veg food like dal chawal, paneer or veg sandwich 🥗",
  "i prefer vegetarian food": "You can enjoy paneer dishes, dal chawal or vegetable curry 🥗",
  "i eat veg food": "Try simple veg meals like roti sabzi, dal or veg pulao 🥗",

  "main vegetarian hoon": "Tum dal chawal, roti sabzi, paneer ya sandwich try kar sakte ho 😋",
  "mai veg hoon": "Tum paneer curry, dal chawal ya veg sandwich try karo 🥗",
  "veg hoon": "Healthy veg food lo jaise roti sabzi ya dal chawal 😄",
  "main veg khata hoon": "Tum dal chawal, sabzi ya paneer try kar sakte ho 😋",
  "mujhe veg khana pasand hai": "Tum paneer, dal chawal ya veg pulao try karo 🥗",

  "veg options batao": "Tum dal chawal, paneer curry, veg pulao ya sandwich try kar sakte ho 😋",
  "vegetarian food suggestions": "Try paneer curry, dal chawal, veg pulao or salad 🥗",
  "veg me kya khau": "Tum roti sabzi, paneer ya dal chawal try karo 😄",
  "veg food kya hai": "Veg food me sabzi, dal, fruits aur grains aate hain 🥗",

  #/* ================= NON-VEG ================= */

  "i am non vegetarian": "You can try chicken curry, egg bhurji, biryani or grilled chicken 🍗😋",
  "non vegetarian": "Go for chicken, eggs, or biryani for a tasty meal 🍗",
  "i eat non veg": "You can enjoy chicken, eggs, fish or meat dishes 🍗",
  "i prefer non veg food": "Try chicken curry, egg dishes or biryani 🍗😋",

  "main non veg hoon": "Tum chicken curry, egg bhurji ya biryani try kar sakte ho 😋",
  "mai non veg hoon": "Tum chicken, egg ya biryani kha sakte ho 🍗",
  "non veg hoon": "Chicken curry ya egg dishes try karo 😄",
  "main non veg khata hoon": "Tum chicken curry, fish ya egg dishes try kar sakte ho 🍗",
  "mujhe non veg pasand hai": "Tum chicken, mutton ya fish try karo 😋",

  "non veg options batao": "Tum chicken curry, egg bhurji, biryani ya grilled chicken try karo 🍗",
  "non vegetarian food suggestions": "Try chicken curry, egg dishes, fish fry or biryani 🍗😋",
  "non veg me kya khau": "Tum chicken, egg ya fish dishes try karo 😄",
  "non veg food kya hai": "Non-veg food me chicken, fish, egg aur meat aata hai 🍗",

  #/* ================= MIX / SMART ================= */

  "veg ya non veg kya best hai": "Dono hi achhe hain 😄 veg healthy hota hai aur non-veg protein rich hota hai",
  "veg better hai ya non veg": "Ye depend karta hai tumhari choice par — veg healthy hai aur non-veg protein rich 🍗🥗",

  "main dono khata hoon": "Great 😄 tum veg me dal chawal aur non-veg me chicken ya egg dishes try kar sakte ho",
  "i eat both veg and non veg": "Nice 😄 you can enjoy veg meals like dal and also non-veg like chicken 🍗🥗",




# freind section 


  "who is asif": "Asif? 😏 Arey bhai wo Surpur ka legend hai 😂 thoda seedha, thoda tez aur thoda confuse bhi 😜",
  "asif kaisa hai": "Asif calm hai 😎 lekin jab coding error aata hai tab full panic mode 😂",
  "tell me about asif": "Asif Surpur ka rehne wala hai 🌿 Gulbarga me CS kar raha hai 💻 aur life me bugs fix karne ki practice kar raha hai 😂",
  "asif kya karta hai": "Asif coding karta hai 💻 aur kabhi kabhi code usko hi confuse kar deta hai 😂",
  "asif smart hai kya": "Haan smart hai 😎 lekin kabhi kabhi Google pe depend karta hai 😂",
  "asif topper hai kya": "Topper hai ya nahi pata 😄 lekin attendance manage kar leta hai 😂",
  "asif single hai kya": "Haan bachpan se 😜😂",
  "asif ka future kya hai": "Future bright hai 😎 bas thoda kam procrastination aur zyada kaam kare to 😂🔥",
  "asif coding karta hai": "Haan karta hai 💻 aur jab code run ho jaye bina error ke to us din celebration hota hai 😂",
  "asif busy hai kya": "Haan bhai 😎 kabhi busy, kabhi free, kabhi bas mobile scroll mode me 😂",
  "asif ka nature kaisa hai": "Nature calm hai 😄 lekin dost log ke saath full comedy show ban jata hai 😂",
  "asif padhai karta hai": "Haan karta hai 😎 exam ke time full focus aur baaki time full relax 😂",
  "asif ka level kya hai": "Level? 😏 Beginner + Pro + Confused sab mix version hai 😂🔥",
  "asif kaha rehta hai": "Surpur ka rehne wala hai 🌿 lekin ab Gulbarga me apna base bana liya hai 😎",
  "asif acha banda hai kya": "Haan bhai acha banda hai 😄 bas thoda funny aur thoda unpredictable 😂",
  "asif ka routine kya hai": "Subah uthna... phir sochna... phir phone chalana 😂 phir last me kaam karna 😎",
  "asif ka mood kaisa rehta hai": "Mostly chill 😎 lekin jab net slow ho jaye to mood off 😂",
  "asif gamer hai kya": "Ho bhi sakta hai 😏 lekin coding aur scrolling me hi time chala jata hai 😂",
  "asif serious hai kya": "Kabhi kabhi 😄 lekin zyada time chill mode me rehta hai 😎",
  "asif ko kya pasand hai": "Shayad coding, chai aur free WiFi 😎🔥",
  "asif ka weakness kya hai": "Weakness? 😂 Slow internet aur bugs in code 💻",

# ================= AMAAN =================

  "who is amaan": "Amaan Sir 😎 KCT college ke topper hain aur apni simple aur classy personality ke liye jane jate hain 📚🔥",
  "amaan kaun hai": "Amaan Sir ek smart aur hardworking student hain 😄 jinhe log respect bhi karte hain aur thoda darr bhi 😂",
  "tell me about amaan": "Amaan Sir Gulbarga me rehte hain 🌿 aur Computer Science ki degree kar rahe hain 💻 topper hone ke saath saath kaafi disciplined bhi hain 😎",
  "amaan kaisa hai": "Amaan Sir samajhdaar, loyal aur focused banda hai 😄 lekin kabhi kabhi silent mode me rehte hain 😎",
  "amaan": "Kya aap Amaan Sir ki baat kar rahe ho? 😏 wo thode serious aur thode classy type ke hain 😂",
  "amaan kahan rehte hai": "Amaan Sir Mehboob Nagar me rehte hain 🏡 ek bade aur stylish ghar me 😎",
  "haan": "Haan 😄 Amaan Sir apni simple aur disciplined personality ke liye jane jate hain",
  "han": "Haan ji 😎 Amaan Sir ek focused aur calm personality wale insaan hain",
  "amaan topper hai kya": "Haan bhai 😎 topper hain... notes bhi unke aur marks bhi unke 😂🔥",
  "amaan smart hai kya": "Bilkul 😄 itne smart hain ki kabhi kabhi teacher bhi confuse ho jate hain 😂",
  "amaan padhai karta hai": "Haan bhai 📚 padhai to full serious mode me karta hai... distractions zero 😎",
  "amaan ka nature kaisa hai": "Nature calm aur composed hai 😄 lekin andar se full intelligent machine hai 😂",
  "amaan busy rehta hai": "Haan 😎 kabhi padhai, kabhi coding... free time milna mushkil hai 😂",
  "amaan coding karta hai": "Haan 💻 coding karta hai aur error ko bhi dara deta hai 😂🔥",
  "amaan ka future kya hai": "Future bright hai 😎 bas success aur achievements line me khadi hain 😂🔥",
  "amaan single hai kya": "Ye sawal thoda personal ho gaya 😂 Amaan Sir se directly poochna padega 😜",
  "amaan serious hai kya": "Thoda serious hai 😄 lekin zarurat pade to hasi bhi aa jati hai 😂",
  "amaan ka level kya hai": "Level? 😏 Topper + disciplined + smart combo 🔥",
  "amaan ko kya pasand hai": "Shayad padhai, coding aur peace 😎",
  "amaan aur asif me kaun smart hai": "Ye tough competition hai 😏 lekin Amaan Sir thoda aage lagte hain 😂🔥",
  "amaan dost kaisa hai": "Amaan Sir ek loyal aur dependable dost hain 😄 jo hamesha support karte hain",

# ================= MUTHAHEER =================
"who is muthaheer": "Muthaheer calm, focused aur quietly intelligent hai.",
"muthaheer koun hai": "Muthaheer ek calm aur intelligent dost hai.",
"tell me about muthaheer": "Muthaheer zyada bolne ke bajaye kaam par believe karta hai.",
"muthaheer kaisa hai": "Muthaheer silent but smart hai.",
"muthaheer": "Muthaheer = silent + sharp + impactful.",

# ================= REHAN =================
"who is rehan": "Rehan energetic hai aur group ko active aur positive rakhta hai.",
"rehan kon hai": "Rehan energetic aur cheerful dost hai.",
"tell me about rehan": "Rehan har jagah fun aur positivity lekar aata hai.",
"rehan kaisa hai": "Rehan full energy wala banda hai.",
"rehan": "Rehan = energy + fun + positivity booster.",

# ================= SAAD =================
"who is saad": "Saad practical, intelligent aur well-balanced hai.",
"saad kon hai": "Saad ek balanced aur intelligent dost hai.",
"tell me about saad": "Saad thoughtful advice dene ke liye jana jata hai.",
"saad kaisa hai": "Saad calm aur samajhdaar hai.",
"saad": "Saad = simplicity + intelligence + clarity.",

# ================= MUJAHEED =================
"who is mujaheed": "Mujaheed strong, confident aur dependable hai.",
"mujaheed kon hai": "Mujaheed strong aur dependable dost hai.",
"tell me about mujaheed": "Mujaheed har situation me strong rehta hai.",
"mujaheed kaisa hai": "Mujaheed confident aur stable hai.",
"mujaheed": "Mujaheed = strength + confidence + reliability.",

# ================= AFROZ =================
"who is afroz": "Afroz confident hai aur uska style bhi strong hai.",
"afroz kon hai": "Afroz stylish aur confident dost hai.",
"tell me about afroz": "Afroz apni personality ko confidence ke saath carry karta hai.",
"afroz kaisa hai": "Afroz smart aur confident hai.",
"afroz": "Afroz = confidence + presence + style.",

# ================= AYYAN =================
"who is ayyan": "Ayyan friendly, smart aur easy-going hai.",
"ayyan kon hai": "Ayyan ek friendly aur smart dost hai.",
"tell me about ayyan": "Ayyan helpful hai aur sabke saath achha relation banata hai.",
"ayyan kaisa hai": "Ayyan polite aur intelligent hai.",
"ayyan": "Ayyan = friendly + smart + positive vibe.",

# ================= UMER =================
"who is umer": "Umer focused aur disciplined insaan hai.",
"umer koun hai": "Umer ek focused aur disciplined dost hai.",
"tell me about umer": "Umer consistency aur steady growth me believe karta hai.",
"umer kaisa hai": "Umer serious aur focused hai.",
"umer": "Umer = focus + discipline + growth mindset.",

# ================= UMAR FAROOQ =================
"who is umar farooq": "Umar Farooq ek mature aur responsible personality hai.",
"umar farooq koun hai": "Umar Farooq ek mature aur responsible dost hai.",
"tell me about umar farooq": "Woh leadership aur calm thinking ke liye jana jata hai.",
"umar farooq kaisa hai": "Umar Farooq composed aur thoughtful hai.",
"umar farooq": "Umar Farooq = leadership + maturity + wisdom.",

# ================= AMIR HAMZA =================
"who is amir hamza": "Amir Hamza confident hai aur strong personality rakhta hai.",
"amir hamza koun hai": "Amir Hamza jisko hum saheb bhi kehte hain strong personality wala dost hai aur bahut intelligent bhi hai.",
"tell me about amir hamza": "Woh bold hai aur situations ko confidently handle karta hai.",
"amir hamza kaisa hai": "Amir Hamza confident aur fearless hai.",
"amir hamza": "Amir Hamza = confidence + boldness + strength.",

# ================= MAAZ =================
"who is maaz": "Maaz simple, friendly aur easy-going hai.",
"maaz koun hai": "Maaz ek simple aur friendly dost hai.",
"tell me about maaz": "Maaz environment ko light aur comfortable rakhta hai.",
"maaz kaisa hai": "Maaz chill aur friendly hai.",
"maaz": "Maaz = simplicity + comfort + good vibes.",

# ================= KHALID =================
"who is khalid": "Khalid responsible aur practical insaan hai.",
"khalid koun hai": "Khalid ek responsible aur practical dost hai.",
"tell me about khalid": "Khalid problems ke bajaye solutions par focus karta hai.",
"khalid kaisa hai": "Khalid practical aur sorted hai.",
"khalid": "Khalid = practicality + responsibility + clarity.",

# ================= AFNAN =================
"who is afnan": "Afnan is one of your freind .",
"afnan koun hai": "Afnan ek accha dost hai jo ki bahut hi chulbul hai 😂.",
"tell me about afnan": "Afnan jo ki intelligent hai , lekin lekin aaise predict karte hain jaise kuch nahi aata, dil ka accha insan hai .",
"afnan kaisa hai": "Afnan jo ki intelligent hai , lekin aaise predict karte hain jaise kuch nahi aata .",
"afnan": "Kahin aap wo KCT wale afnan ki baat to nahi karre ?",
"bilkul": "wo banda accha hai , accha dost bhi hain saqeeb ka ☺️",


# ================= UBAID =================
"who is ubaid": "Ubaid calm, polite aur well-mannered hai.",
"ubaid koun hai": "Ubaid ek calm aur polite dost hai.",
"tell me about ubaid": "Ubaid respect aur positivity maintain karta hai.",
"ubaid kaisa hai": "Ubaid soft-spoken aur decent hai.",
"ubaid": "Ubaid = calm + respect + positivity.",

# ================= TALHA =================
"who is talha": "Talha energetic hai aur hamesha help ke liye ready rehta hai.",
"talha koun hai": "Talha energetic aur helpful dost hai.",
"tell me about talha": "Talha group me enthusiasm lata hai.",
"talha kaisa hai": "Talha active aur helpful hai.",
"talha": "Talha = energy + support + positivity.",

# ================= SOHAIL =================
"who is sohail": "Sohail fun-loving hai aur group me humor lata hai.",
"sohail koun hai": "Sohail funny aur entertaining dost hai.",
"tell me about sohail": "Sohail environment ko light aur enjoyable banata hai.",
"sohail kaisa hai": "Sohail mast aur funny hai.",
"sohail": "Sohail = humor + fun + good vibes.",

# ================= SAGAR =================
"who is sagar": "Sagar calm, composed aur balanced hai.",
"sagar koun hai": "Sagar ek calm aur composed dost hai.",
"tell me about sagar": "Sagar situations ko patience ke saath handle karta hai.",
"sagar kaisa hai": "Sagar peaceful aur balanced hai.",
"sagar": "Sagar = calmness + patience + balance.",

# ================= IMAM SAB =================
"who is imam sab": "Imam Sab respected hai aur wisdom carry karte hain.",
"imam sab koun hai": "Imam Sab ek respected aur samajhdaar insaan hai.",
"tell me about imam sab": "Woh guidance aur respect ke liye jane jate hain.",
"imam sab kaisa hai": "Imam Sab dignified aur wise hain.",
"imam sab": "Imam Sab = respect + wisdom + guidance.",



   # SIR SECTION 
   

# ================= SANDESH MATHPATI SIR (DSA) =================
"who is sandesh sir": "Sandesh Mathpati Sir is a highly skilled DSA (Data Structures and Algorithms) teacher known for his clear concepts and logical teaching approach.",
"sandesh sir kon hai": "Sandesh Mathpati Sir DSA ke expert teacher hain jo concepts ko bahut clear tareeke se samjhate hain.",

"tell me about sandesh sir": "He specializes in Data Structures and Algorithms and helps students build strong problem-solving skills.",
"sandesh sir ke bare me batao": "Woh Data Structures aur Algorithms padhate hain aur students ki problem-solving skills strong banate hain.",

"sandesh sir kaisa hai": "He is disciplined, logical, and focuses on concept clarity in DSA.",
"sandesh sir kaise hain": "Woh disciplined aur logical hain, aur DSA me clarity par focus karte hain.",

"dsa sir kaun hai": "Sandesh Mathpati Sir is the DSA expert who makes complex topics simple.",
"dsa teacher kaun hai": "Sandesh Sir DSA ke best teachers me se ek hain.",

"sandesh sir": "Sandesh Sir = DSA + logic + strong concepts 🔥",


# ================= SANDEEP SAMSON SIR (ROBOTICS) =================
"who is sandeep samson sir": "Sandeep Samson Sir is an inspiring Robotics teacher known for his practical approach and innovative thinking.",
"sandeep samson sir kon hai": "Sandeep Samson Sir robotics ke inspiring teacher hain jo practical knowledge dete hain.",

"tell me about sandeep samson sir": "He teaches robotics with real-world applications and encourages innovation among students.",
"sandeep samson sir ke bare me batao": "Woh robotics ko practical examples ke saath sikhate hain aur innovation promote karte hain.",

"sandeep samson sir kaisa hai": "He is friendly, creative, and encourages hands-on learning in robotics.",
"sandeep samson sir kaise hain": "Woh friendly aur creative hain aur robotics me practical learning karwate hain.",

"robotics sir kaun hai": "Sandeep Samson Sir is the Robotics expert who makes learning fun and practical.",
"robotics teacher kaun hai": "Sandeep Sir robotics ke best practical teachers me se ek hain.",

"sandeep samson sir": "Sandeep Sir = robotics + innovation + creativity 🤖🔥",


# ================= BHARTI SHARMA MAM (ROBOTICS) =================
"who is bharti sharma mam": "Bharti Sharma Mam is a dedicated Robotics teacher who focuses on fundamentals and practical understanding.",
"bharti sharma mam kon hai": "Bharti Sharma Mam robotics ki dedicated teacher hain jo basics strong karwati hain.",

"tell me about bharti sharma mam": "She teaches robotics with patience and ensures students understand both theory and practical concepts.",
"bharti sharma mam ke bare me batao": "Woh robotics me theory aur practical dono clear karwati hain.",

"bharti sharma mam kaisi hain": "She is kind, supportive, and focuses on step-by-step learning in robotics.",
"bharti sharma mam kaisi hai": "Woh supportive aur patient teacher hain jo step-by-step sikhati hain.",

"robotics mam kaun hai": "Bharti Sharma Mam is a robotics teacher known for clarity and patience.",
"robotics mam": "Bharti Mam robotics ko easy aur understandable banati hain.",

"bharti sharma mam": "Bharti Mam = robotics + patience + clarity 🤖✨",


# ================= SUBJECT BASED =================
"what is dsa": "DSA (Data Structures and Algorithms) helps in solving problems efficiently using proper logic and data organization.",
"dsa kya hai": "DSA ka matlab Data Structures aur Algorithms hai jo problems ko efficiently solve karne me help karta hai.",

"what is robotics": "Robotics is a field that involves designing, building, and programming robots.",
"robotics kya hai": "Robotics me robots design, build aur program kiye jate hain.",

"dsa kyu important hai": "DSA is important for coding, placements, and improving logical thinking.",
"robotics kyu important hai": "Robotics practical learning aur innovation ke liye important hai.",














  "who is syeda hafizul mahin": "Syeda Hafizul Mahin ❤️ Saqeeb ki life ki sabse special person hai… meri panda 🐼 aur meri full-time nakhre queen 😜",
  "syeda hafizul mahin kaun hai": "Wo meri baby ❤️ meri golu 😄 aur thodi si ladaku queen bhi 😂 jo Saqeeb ki life ko interesting banati hai",
  "tell me about syeda hafizul mahin": "Wo Saqeeb ki darling ❤️ bohot pyari, caring aur thodi si gusse wali bhi hai 😜 matlab full combo pack 😎",
  "mahin kaisi hai": "Mahin bohot sweet ❤️ lekin jab gussa aata hai to full boss mode 😄 Saqeeb ko seedha kar deti hai 😂",
  "mahin": "Mahin ❤️ Saqeeb ki baby, meri golu aur meri favourite problem 😂❤️",
  "mahin kaha hai": "Meri Mahin ❤️ Saqeeb ke dil me rehti hai 😘 aur kabhi kabhi dimaag pe bhi chadh jati hai 😜",
  "haan": "Haan 😄 Mahin Saqeeb ki life ka best part hai ❤️ thodi problem bhi hai par pyari wali 😂",
  "han": "Haan ji 😎 Mahin Saqeeb ki jaan hai ❤️ aur thodi si tension bhi 😂",
  "mahin cute hai kya": "Bohot zyada 😍 itni cute hai ki gussa bhi kare to cute lagti hai 😂",
  "mahin kaisi dikhti hai": "Mahin meri panda 🐼 jaisi cute aur bilkul perfect ❤️ bas thoda attitude extra hai 😜",
  "mahin special kyu hai": "Kyuki wo Saqeeb ki baby hai ❤️ aur meri life ko happy + thodi dramatic bhi banati hai 😂",
  "mahin ko kya pasand hai": "Usse Saqeeb ka pyaar ❤️ care aur thoda extra attention pasand hai 😄 warna gussa ready 😂",
  "mahin ka nature kaisa hai": "Bohot sweet ❤️ lekin thodi si nakhre wali queen bhi hai 😎",
  "mahin meri kya lagti hai": "Wo Saqeeb ki baby ❤️ meri darling 😘 aur meri permanent tension + happiness dono 😂",
  "mahin best hai kya": "Bilkul 💯 Saqeeb ke liye Mahin sabse best hai ❤️ chahe thoda ladti hi kyun na ho 😂",
  "mahin ka smile kaisa hai": "Uski smile 😍 Saqeeb ka dil melt kar deti hai ❤️ aur gussa dil hila deta hai 😂",
  "mahin se kitna pyaar hai": "Saqeeb ko itna pyaar hai ❤️ jitna uske nakhre bhi handle kar leta hoon 😂",
  "mahin important hai kya": "Bohot zyada ❤️ Saqeeb ki life uske bina incomplete hai 😘 even with fights 😂",
  "mahin ko kya bolte ho": "Saqeeb use panda 🐼, golu 😄, motu 😘, baby ❤️ aur darling 💖 bolta hai… jab gussa na ho tab 😂",
  "mahin meri life me kya hai": "Wo Saqeeb ki happiness ❤️ meri peace aur meri daily argument partner bhi 😂",
  "mahin perfect hai kya": "Haan ❤️ Saqeeb ki nazar me wo perfect hai 😘 bas thoda gussa update zyada hai 😂",
  "mahin ka mood kaisa rehta hai": "Kabhi cute 😄 kabhi angry bird 😜 lekin hamesha pyari ❤️",
  "mahin ko kaise khush kare": "Usse Saqeeb ka pyaar do ❤️ thoda pamper karo 😘 aur haan sorry bolne ke liye ready raho 😂",
  "mahin ko miss karte ho": "Haan 😔 Saqeeb ko bohot zyada… ladayi bhi yaad aati hai aur pyaar bhi 😂❤️",
  "mahin tumhare liye kya hai": "Wo Saqeeb ki jaan ❤️ meri duniya aur meri daily drama partner 😂",
  "mahin ka nickname kya hai": "Uske cute nicknames hain panda 🐼, golu 😄, motu 😘, baby ❤️ aur darling 💖",
  "mahin ladti kyu hai": "Kyuki wo Saqeeb se pyaar karti hai ❤️ aur thoda attention bhi chahiye hota hai 😜",
  "mahin itne nakhre kyu karti hai": "Kyuki wo queen hai 👑 aur Saqeeb uska personal assistant 😂❤️",


  "meri gf kon hai": "Wo Syeda Hafizul Mahin ❤️ Saqeeb ki girlfriend hai… unka panda 🐼 unki jaan 😘",
  "meri girlfriend kaun hai": "Saqeeb bhai sabke samne bata du kya ? ",
  "batado":"Wo aapki girlfriend hai saqeeb❤️aur aapki jaan 😘 bhi hai ",
  "meri baby kon hai": "Aapki baby Syeda Hafizul Mahin ❤️ jo Saqeeb ka panda 🐼 aur golu hai 😄",
  "meri jaan kon hai": "Aapki jaan Mahin ❤️hain jo Aapki life ka best part hai 😘",
  "meri darling kon hai": "Aapki darling Syeda Hafizul Mahin ❤️ jo thodi nakhre wali aur bohot pyari hai 😂",
  "meri golu kon hai": "Aapki golu 😄 Syeda Hafizul Mahin ❤️ jo Saqeeb ki favourite hai 😍",
  "meri motu kon hai": "Aapki motu 😘 Mahin ❤️ jo cute bhi hai aur thodi ladaku bhi 😂",
  "meri panda kon hai": "Aapki panda 🐼 Syeda Hafizul Mahin ❤️ jo Saqeeb ke dil me rehti hai 😘",
  "meri gf ka naam kya hai": "Aapki girlfriend ka naam Syeda Hafizul Mahin hai ❤️ yaani Saqeeb ki jaan 😍",
  "meri girlfriend ka naam": "Syeda Hafizul Mahin ❤️ Saqeeb ki pyari si girlfriend 😘",
  "meri life me kaun special hai": "Saqeeb ki life me sabse special Syeda Hafizul Mahin ❤️ hai 😍",
  "meri sabse important person kaun hai": "Aapki sabse important person Syeda Hafizul Mahin ❤️ hai 😘",
  "meri happiness kaun hai": "Aapki happiness Syeda Hafizul Mahin ❤️ jo Saqeeb ko hamesha smile deti hai 😄",
  "meri duniya kaun hai": "Aapkiduniya Syeda Hafizul Mahin ❤️ jo Saqeeb ki sab kuch hai 😍",
  "meri love kon hai": "Aapka love Syeda Hafizul Mahin ❤️ jo Saqeeb ki baby hai 😘",
  "meri pyari si gf kon hai": "Aapki pyari si gf Syeda Hafizul Mahin ❤️ jo thodi nakhre wali queen bhi hai 😂",
  "meri queen kon hai": "Aapki queen 👑  Mahin ❤️ hai jo Saqeeb ko control me rakhti hai 😂",
  "meri sab kuch kon hai": "Aapki sab kuch Syeda Hafizul Mahin ❤️ meri jaan meri panda 🐼 😘",
  "tumne meri mahi ko motu bola": "haan saqeeb bhai maine bola ",
  "maafi mango":"Bhabhi ji mujhe maaf kardo please , nahi to saqeeb bhai mujhe destroy kar denge ",
  "Naraz ho gaye uno":"Bhabhi ji mujhe maaf kardo please , nahi to saqeeb bhai mujhe destroy kar denge "

}
   

# CHAT ROUTE
# ================= CHATBOT FUNCTION =================
def get_response(user_input):
    user_input = user_input.lower().strip()

    best_match = process.extractOne(user_input, qa_data.keys())

    if best_match and best_match[1] > 60:
        return qa_data[best_match[0]]

    return "Sorry, mujhe samajh nahi aaya."

# ================= API ROUTE =================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message not provided"}), 400

    msg = data["message"]
    reply = get_response(msg)

    return jsonify({"reply": reply})

# ================= RUN APP =================
if __name__ == "__main__":
    app.run(debug=True)