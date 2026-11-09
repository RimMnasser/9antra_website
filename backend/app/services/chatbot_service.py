import pandas as pd
from sentence_transformers import SentenceTransformer, util
from langdetect import detect
from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import wordnet
import re
from pathlib import Path
import torch


class ChatbotService:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent.parent / "export_chatbot"

        # Téléchargement WordNet si nécessaire
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
            nltk.download('omw-1.4')

        print("📥 Chargement des fichiers Excel...")
        self._load_dataframes()

        print("⏳ Chargement du modèle et pré-encodage...")
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self._prepare_intents_and_embeddings()

        print("✅ ChatbotService prêt")

    def _load_dataframes(self):
        self.df = pd.read_excel(self.base_path / "services.xlsx")
        self.df['description'] = self.df['description'].fillna("")
        self.df['name'] = self.df['name'].fillna("")

        self.df_events = pd.read_excel(self.base_path / "events.xlsx")
        self.df_events['name_event'] = self.df_events['name_event'].fillna("")
        self.df_events['date_event'] = pd.to_datetime(self.df_events['date_event'], errors='coerce')
        self.df_events['participants'] = pd.to_numeric(self.df_events['participants'], errors='coerce').fillna(0).astype(int)
        self.df_events['interested'] = pd.to_numeric(self.df_events['interested'], errors='coerce').fillna(0).astype(int)
        self.df_events['Status_event'] = pd.to_numeric(self.df_events['Status_event'], errors='coerce').fillna(0).astype(int)

        self.df_posts = pd.read_excel(self.base_path / "posts_nettoye (1).xlsx")
        self.df_posts['description'] = self.df_posts['description'].fillna("")
        self.df_posts['likes'] = pd.to_numeric(self.df_posts['likes'], errors='coerce').fillna(0).astype(int)
        self.df_posts['shares'] = pd.to_numeric(self.df_posts['shares'], errors='coerce').fillna(0).astype(int)
        self.df_posts['comments'] = pd.to_numeric(self.df_posts['comments'], errors='coerce').fillna(0).astype(int)
        self.df_posts['post_date'] = pd.to_datetime(self.df_posts['post_date'], errors='coerce')

    def _prepare_intents_and_embeddings(self):
        self.intents_examples = {
            "intent_web": [
                "formation site web", "apprendre angular", "développeur react", "web development",
                "full stack js", "node js", "spring boot", "créer un site internet", "front end back end"
            ],
            "intent_mobile": [
                "application mobile", "formation flutter", "développer une app", "mobile app",
                "android", "ios", "application téléphone"
            ],
            "intent_data_ia": [
                "intelligence artificielle", "machine learning", "deep learning", "artificial intelligence",
                "data analytics", "power bi", "business intelligence", "big data", "tableau de bord"
            ],
            "intent_iot": [
                "objets connectés", "capteurs", "protocole mqtt", "internet of things", "iot",
                "systèmes embarqués"
            ],
            "intent_pfe": [
                "préparer mon pfe", "stage de fin d'études", "aide pour le mémoire", "pfe preparation",
                "trouver un sujet de pfe", "accompagnement pfe", "fin d'études"
            ],
            "intent_bootcamp": [
                "formation intensive", "bootcamp d'été", "summer camp", "formation rapide",
                "stage d'été", "booster mes compétences"
            ],
            "intent_supervision": [
                "supervision", "suivi individuel", "aide au debugging", "tuteur", "résoudre des erreurs",
                "coaching personnalisé"
            ],
            "intent_prix": [
                "combien ça coûte", "quel est le prix", "tarif", "how much", "price", "coût ",
                "moins cher", "budget"
            ],
            "intent_duree": [
                "combien de temps", "durée ", "ça dure combien", "how long", "nombre de mois",
                "nombre d'heures", "calendrier"
            ],
            "intent_rythme": [
                "combien d'heures par semaine", "rythme", "emploi du temps", "cours en ligne", "présentiel",
                "hybride", "combien de cours par semaine"
            ],
            "intent_event_liste": [
                "liste des événements", "quels événements", "montre les événements",
                "tous les événements", "liste events", "quelles sont les événements", "les événements disponibles",
                "les événements existantes", "donne moi la liste des events", "quels workshops", "liste des workshops"
            ],
            "intent_event_date": [
                "date de l'événement", "quand est l'événement", "quelle est la date",
                "quand a lieu", "quand se déroule", "quel jour", "c'était quand", "donne moi la date", "dis moi quand"
            ],
            "intent_event_participants": [
                "nombre de participants", "combien de participants", "combien étaient là",
                "combien ont participé", "combien de personnes sont venues", "combien de gens ont assisté", "effectif du workshop"
            ],
            "intent_event_total_participants": [
                "total des participants", "tous les participants", "somme des participants",
                "combien de participants en tout", "nombre total de participants", "total global des participants"
            ],
            "intent_event_interested": [
                "nombre d'intéressés", "combien d'intéressés", "combien de personnes intéressées",
                "combien de gens étaient intéressés", "combien ont montré de l'intérêt"
            ],
            "intent_event_status_termine": [
                "événement terminé", "events terminés", "liste événements terminés",
                "quels événements sont terminés", "montre les events terminés"
            ],
            "intent_event_max_participants": [
                "quel événement a le plus de participants", "event avec le plus de participants",
                "le plus grand événement", "événement le plus populaire", "quel est l'événement le plus suivi", "top événement participants"
            ],
            "intent_event_status_encours": [
                "événement en cours", "events en cours", "liste événements en cours",
                "quels événements sont en cours", "montre les events en cours"
            ],
            "intent_post_likes": [
                "likes du post", "combien de likes", "nombre de likes", "combien de j'aime", "likes pour ce post"
            ],
            "intent_post_shares": [
                "shares du post", "combien de partages", "nombre de partages", "combien de shares", "partages pour ce post"
            ],
            "intent_post_comments": [
                "commentaires du post", "combien de commentaires", "nombre de commentaires",
                "combien de comments", "commentaires pour ce post"
            ],
            "intent_post_total_likes": [
                "total des likes", "somme des likes", "tous les likes", "combien de likes en tout", "nombre total de likes"
            ],
            "intent_post_total_shares": [
                "total des partages", "somme des partages", "tous les partages", "combien de partages en tout", "nombre total de shares"
            ],
            "intent_post_max_likes": [
                "post avec le plus de likes", "quel post a le plus de likes", "le post le plus liké", "top likes", "post le plus populaire"
            ],
            "intent_post_sans_desc": [
                "combien de posts sans description", "posts sans description", "nombre de posts vides", "posts sans texte", "combien de posts sans contenu"
            ],
            "intent_post_min_likes": [
                "post le moins liké", "quel post a le moins de likes", "le post avec le minimum de likes", "post le moins populaire"
            ],
            "intent_post_max_shares": [
                "post avec le plus de partages", "quel post a le plus de shares", "le post le plus partagé", "top shares",
                "post le plus partagé", "maximum de shares", "maximum de partages", "le post avec le maximum de shares",
                "post le plus share", "le maximum de partage"
            ],
            "intent_post_min_shares": [
                "post le moins partagé", "quel post a le moins de partages", "le post avec le minimum de shares",
                "post le moins partagé", "minimum de partages", "moins de shares", "le minimum de partage"
            ]
        }

        self.intent_labels = []
        self.intent_phrases = []
        for intent, phrases in self.intents_examples.items():
            for p in phrases:
                self.intent_phrases.append(p)
                self.intent_labels.append(intent)

        self.intent_embeddings = self.model.encode(self.intent_phrases, convert_to_tensor=True)
        self.noms_events_list = self.df_events['name_event'].tolist()
        self.events_embeddings = self.model.encode(self.noms_events_list, convert_to_tensor=True)
        self.posts_desc_embeddings = self.model.encode(self.df_posts['description'].tolist(), convert_to_tensor=True)

    # ==========================================
    # FONCTIONS DE TRADUCTION
    # ==========================================
    def detecter_langue(self, texte):
        try:
            return detect(texte)
        except:
            return 'fr'

    def traduire_vers_francais(self, texte):
        try:
            return GoogleTranslator(source='auto', target='fr').translate(texte)
        except:
            return texte

    def traduire_vers_anglais(self, texte):
        try:
            return GoogleTranslator(source='auto', target='en').translate(texte)
        except:
            return texte

    def traduire_reponse_finale(self, texte_fr, langue_cible):
        if langue_cible != 'fr':
            try:
                return GoogleTranslator(source='fr', target=langue_cible).translate(texte_fr)
            except:
                return texte_fr
        return texte_fr

    # ==========================================
    # SYNONYMES
    # ==========================================
    def get_synonyms_wordnet(self, word):
        synonyms = set()
        for syn in wordnet.synsets(word, lang='eng'):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().replace('_', ' '))
        return list(synonyms)

    def texte_contient_synonyme(self, text_en, mots_base):
        for mot in mots_base:
            syns = self.get_synonyms_wordnet(mot)
            syns.append(mot)
            for syn in syns:
                if syn in text_en:
                    return True
        return False

    # ==========================================
    # RECHERCHE ÉVÉNEMENT
    # ==========================================
    def trouver_event_par_nom(self, nom_recherche):
        nom_recherche = nom_recherche.lower().strip()

        for _, row in self.df_events.iterrows():
            if nom_recherche in str(row['name_event']).lower():
                return row.to_dict()

        nom_embedding = self.model.encode(nom_recherche, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(nom_embedding, self.events_embeddings)[0]
        meilleur_idx = scores.argmax().item()
        meilleur_score = scores[meilleur_idx].item()

        if meilleur_score > 0.5:
            return self.df_events.iloc[meilleur_idx].to_dict()
        return None

    # ==========================================
    # DÉTECTION D'INTENTION (ton code exact)
    # ==========================================
    def detecter_intention_hybride(self, texte_fr):
        text_fr = texte_fr.lower()
        text_en = self.traduire_vers_anglais(text_fr)

        if "en cours" in text_fr and any(m in text_fr for m in ["événement", "event"]):
            return "intent_event_status_encours"
        if any(m in text_fr for m in ["terminé", "terminée"]) and any(m in text_fr for m in ["événement", "event"]):
            return "intent_event_status_termine"

        user_emb = self.model.encode(texte_fr, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(user_emb, self.intent_embeddings)[0]
        if scores.max().item() > 0.6:
            return self.intent_labels[scores.argmax().item()]

        mots_demande = ["détail", "detail", "information", "programme", "contenu", "décris", "explique"]
        if any(mot in text_fr for mot in mots_demande):
            if "ia" in text_fr or "intelligence artificielle" in text_fr or "data" in text_fr:
                return "intent_data_ia"
            if "web" in text_fr or "site" in text_fr:
                return "intent_web"
            if "iot" in text_fr or "objet connecté" in text_fr:
                return "intent_iot"
            if "mobile" in text_fr or "application" in text_fr:
                return "intent_mobile"
            if "pfe" in text_fr or "mémoire" in text_fr:
                return "intent_pfe"
            if "bootcamp" in text_fr:
                return "intent_bootcamp"
            if "supervision" in text_fr:
                return "intent_supervision"

        if self.texte_contient_synonyme(text_en, ['web', 'website', 'site']) and self.texte_contient_synonyme(text_en, ['develop', 'build', 'apprendre']):
            return "intent_web"
        if self.texte_contient_synonyme(text_en, ['mobile', 'app', 'phone']) and self.texte_contient_synonyme(text_en, ['develop', 'build', 'apprendre']):
            return "intent_mobile"
        if self.texte_contient_synonyme(text_en, ['artificial', 'machine learning', 'deep learning', 'data', 'bi']):
            return "intent_data_ia"
        if self.texte_contient_synonyme(text_en, ['iot', 'internet of things', 'sensor', 'capteur']):
            return "intent_iot"

        if "pfe" in text_fr or "mémoire" in text_fr or "fin d'étude" in text_fr:
            return "intent_pfe"
        if "bootcamp" in text_fr or "été" in text_fr or "intensif" in text_fr:
            return "intent_bootcamp"
        if "supervision" in text_fr or "tuteur" in text_fr or "debug" in text_fr:
            return "intent_supervision"

        if self.texte_contient_synonyme(text_en, ['price', 'cost', 'cheap', 'expensive']) or "prix" in text_fr or "coût" in text_fr or "dt" in text_fr:
            return "intent_prix"
        if self.texte_contient_synonyme(text_en, ['long', 'duration', 'month', 'time']) or "durée" in text_fr or "combien de temps" in text_fr:
            return "intent_duree"
        if self.texte_contient_synonyme(text_en, ['hour', 'week', 'schedule', 'pace']) or "heure" in text_fr or "rythme" in text_fr or "par semaine" in text_fr:
            return "intent_rythme"

        if any(m in text_fr for m in ["date", "quand", "quel jour"]):
            if any(m in text_fr for m in ["événement", "event", "workshop", "formation", "bootcamp", "summer camp"]):
                return "intent_event_date"

        if any(m in text_fr for m in ["plus de participants", "le plus grand", "le plus populaire", "top événement"]):
            return "intent_event_max_participants"

        if any(m in text_fr for m in ["participant", "personnes présentes", "ont participé", "étaient là"]):
            if "total" not in text_fr and "tous" not in text_fr and "en tout" not in text_fr:
                return "intent_event_participants"

        if any(m in text_fr for m in ["total", "tous", "toutes", "en tout", "somme"]):
            if "participant" in text_fr:
                return "intent_event_total_participants"

        if any(m in text_fr for m in ["intéressé", "intéressée", "intéressés"]):
            return "intent_event_interested"

        if any(m in text_fr for m in ["terminé", "terminée"]):
            if any(m in text_fr for m in ["événement", "event"]):
                return "intent_event_status_termine"

        if "en cours" in text_fr:
            if any(m in text_fr for m in ["événement", "event"]):
                return "intent_event_status_encours"

        if "sans description" in text_fr or "sans texte" in text_fr or "posts vides" in text_fr:
            return "intent_post_sans_desc"

        if "total" in text_fr and "like" in text_fr:
            return "intent_post_total_likes"
        if "total" in text_fr and ("partage" in text_fr or "share" in text_fr):
            return "intent_post_total_shares"
        if "plus de like" in text_fr or "le plus liké" in text_fr or "top like" in text_fr:
            return "intent_post_max_likes"
        if "plus de partage" in text_fr or "le plus partagé" in text_fr or "top share" in text_fr:
            return "intent_post_max_shares"
        if "commentaire" in text_fr or "comment" in text_fr:
            return "intent_post_comments"
        if "like" in text_fr:
            return "intent_post_likes"
        if "partage" in text_fr or "share" in text_fr:
            return "intent_post_shares"
        if "moins de like" in text_fr or "le moins liké" in text_fr or "minimum de like" in text_fr:
            return "intent_post_min_likes"
        if "moins de partage" in text_fr or "le moins partagé" in text_fr or "minimum de share" in text_fr:
            return "intent_post_min_shares"

        return None

    # ==========================================
    # GÉNÉRATION DE RÉPONSE (ton code exact)
    # ==========================================
    def generer_reponse_structuree(self, user_input_fr, intention):
        if intention not in [
            "intent_web", "intent_mobile", "intent_data_ia", "intent_iot",
            "intent_bootcamp", "intent_supervision", "intent_prix",
            "intent_duree", "intent_rythme",
            "intent_event_date", "intent_event_participants", "intent_event_total_participants",
            "intent_event_interested", "intent_event_status_termine", "intent_event_status_encours",
            "intent_event_liste", "intent_event_max_participants",
            "intent_post_likes", "intent_post_shares", "intent_post_comments",
            "intent_post_total_likes", "intent_post_total_shares",
            "intent_post_max_likes", "intent_post_max_shares", "intent_post_sans_desc",
            "intent_post_min_likes", "intent_post_min_shares"
        ]:
            return None

        def trouver_post_par_sujet(question, colonne_retour):
            mots_vides = ["likes", "like", "partages", "partage", "shares", "share",
                          "commentaires", "commentaire", "comments", "comment",
                          "combien", "nombre", "de", "du", "pour", "le", "la", "les",
                          "post", "quel", "quelle", "un", "une", "des"]
            sujet = question.lower()
            for m in mots_vides:
                sujet = re.sub(r'\b' + re.escape(m) + r'\b', '', sujet, flags=re.IGNORECASE)
            sujet = re.sub(r'\s+', ' ', sujet).strip()

            if len(sujet) < 2:
                return None

            mots_sujet = [m for m in sujet.split() if len(m) > 2]
            candidats = self.df_posts[self.df_posts['description'].str.lower().apply(
                lambda d: any(m in d for m in mots_sujet)
            )]

            if candidats.empty:
                return None

            cand_emb = self.model.encode(candidats['description'].tolist(), convert_to_tensor=True)
            sujet_emb = self.model.encode(sujet, convert_to_tensor=True)
            scores = util.pytorch_cos_sim(sujet_emb, cand_emb)[0]
            idx = scores.argmax().item()

            if scores[idx].item() > 0.3:
                post = candidats.iloc[idx]
                desc_courte = str(post['description'])[:80] + "..." if len(str(post['description'])) > 80 else post['description']
                return f"**{post[colonne_retour]}|{desc_courte}"
            return None

        # --- POSTS ---
        if intention == "intent_post_likes":
            resultat = trouver_post_par_sujet(user_input_fr, 'likes')
            if not resultat:
                return "❌ Post non trouvé. Précisez le sujet."
            nb, desc = resultat.split("|", 1)
            return f"👍 **{nb}** likes pour le post :\n> {desc}"

        if intention == "intent_post_shares":
            resultat = trouver_post_par_sujet(user_input_fr, 'shares')
            if not resultat:
                return "❌ Post non trouvé. Précisez le sujet."
            nb, desc = resultat.split("|", 1)
            return f"🔄 **{nb}** partages pour le post :\n> {desc}"

        if intention == "intent_post_comments":
            resultat = trouver_post_par_sujet(user_input_fr, 'comments')
            if not resultat:
                return "❌ Post non trouvé. Précisez le sujet."
            nb, desc = resultat.split("|", 1)
            return f"💬 **{nb}** commentaires pour le post :\n> {desc}"

        if intention == "intent_post_sans_desc":
            sans_desc = self.df_posts[
                (self.df_posts['description'].str.strip() == "") |
                (self.df_posts['description'].str.lower().str.contains("pas de description"))
            ]
            return f"📝 Posts sans description : **{len(sans_desc)}** sur {len(self.df_posts)} posts"

        if intention == "intent_post_total_likes":
            total = self.df_posts['likes'].sum()
            return f"📊 Total des likes (tous posts) : **{total}**"

        if intention == "intent_post_total_shares":
            total = self.df_posts['shares'].sum()
            return f"📊 Total des partages (tous posts) : **{total}**"

        if intention == "intent_post_max_likes":
            idx_max = self.df_posts['likes'].idxmax()
            post = self.df_posts.iloc[idx_max]
            d = post['post_date'].strftime('%d/%m/%Y') if pd.notna(post['post_date']) else "N/A"
            desc_courte = str(post['description'])[:80] + "..." if len(str(post['description'])) > 80 else post['description']
            return f"🏆 **Post le plus liké** ({post['likes']} likes)\n📅 {d}\n> {desc_courte}"

        if intention == "intent_post_max_shares":
            idx_max = self.df_posts['shares'].idxmax()
            post = self.df_posts.iloc[idx_max]
            d = post['post_date'].strftime('%d/%m/%Y') if pd.notna(post['post_date']) else "N/A"
            desc_courte = str(post['description'])[:80] + "..." if len(str(post['description'])) > 80 else post['description']
            return f"🏆 **Post le plus partagé** ({post['shares']} partages)\n📅 {d}\n> {desc_courte}"

        if intention == "intent_post_min_likes":
            idx_min = self.df_posts['likes'].idxmin()
            post = self.df_posts.iloc[idx_min]
            d = post['post_date'].strftime('%d/%m/%Y') if pd.notna(post['post_date']) else "N/A"
            desc_courte = str(post['description'])[:80] + "..." if len(str(post['description'])) > 80 else post['description']
            return f"📉 **Post le moins liké** ({post['likes']} likes)\n📅 {d}\n> {desc_courte}"

        if intention == "intent_post_min_shares":
            idx_min = self.df_posts['shares'].idxmin()
            post = self.df_posts.iloc[idx_min]
            d = post['post_date'].strftime('%d/%m/%Y') if pd.notna(post['post_date']) else "N/A"
            desc_courte = str(post['description'])[:80] + "..." if len(str(post['description'])) > 80 else post['description']
            return f"📉 **Post le moins partagé** ({post['shares']} partages)\n📅 {d}\n> {desc_courte}"

        # --- EVENTS ---
        if intention == "intent_event_liste":
            reponse = f"📋 **Tous les événements** ({len(self.df_events)}) :\n\n"
            for i, (_, e) in enumerate(self.df_events.iterrows(), 1):
                d = e['date_event'].strftime('%d/%m/%Y') if pd.notna(e['date_event']) else "N/A"
                reponse += f"{i}. **{e['name_event']}** | {d}\n"
            return reponse.strip()

        if intention == "intent_event_max_participants":
            idx_max = self.df_events['participants'].idxmax()
            event = self.df_events.loc[idx_max]
            d = event['date_event'].strftime('%d/%m/%Y') if pd.notna(event['date_event']) else "N/A"
            return f"🏆 **{event['name_event']}**\n📅 {d}\n👥 {event['participants']} participants (le maximum)"

        if intention == "intent_event_date":
            event = self.trouver_event_par_nom(user_input_fr)
            if event is None:
                return "❌ Événement non trouvé."
            date_str = event['date_event'].strftime('%d/%m/%Y') if pd.notna(event['date_event']) else "N/A"
            return f"📅 **{event['name_event']}** → {date_str}"

        if intention == "intent_event_participants":
            event = self.trouver_event_par_nom(user_input_fr)
            if event is None:
                return "❌ Événement non trouvé."
            return f"👥 **{event['name_event']}** → {event['participants']} participants"

        if intention == "intent_event_total_participants":
            total = self.df_events['participants'].sum()
            return f"📊 Total participants (tous événements) : **{total}** personnes"

        if intention == "intent_event_interested":
            event = self.trouver_event_par_nom(user_input_fr)
            if event is None:
                return "❌ Événement non trouvé."
            return f"❤️ **{event['name_event']}** → {event['interested']} intéressés"

        if intention == "intent_event_status_termine":
            events_filtres = self.df_events[self.df_events['Status_event'] == 0]
            if events_filtres.empty:
                return "📭 Aucun événement terminé."
            reponse = f"📋 **Événements terminés** ({len(events_filtres)}) :\n\n"
            for i, (_, e) in enumerate(events_filtres.head(10).iterrows(), 1):
                d = e['date_event'].strftime('%d/%m/%Y') if pd.notna(e['date_event']) else "N/A"
                reponse += f"{i}. **{e['name_event']}** | {d} | {e['participants']} participants\n"
            if len(events_filtres) > 10:
                reponse += f"\n... et {len(events_filtres) - 10} autres"
            return reponse.strip()

        if intention == "intent_event_status_encours":
            events_filtres = self.df_events[self.df_events['Status_event'] == 1]
            if events_filtres.empty:
                return "📭 Aucun événement en cours."
            reponse = f"📋 **Événements en cours** ({len(events_filtres)}) :\n\n"
            for i, (_, e) in enumerate(events_filtres.iterrows(), 1):
                d = e['date_event'].strftime('%d/%m/%Y') if pd.notna(e['date_event']) else "N/A"
                reponse += f"{i}. **{e['name_event']}** | {d} | {e['participants']} participants\n"
            return reponse.strip()

        # --- SERVICES / FORMATIONS ---
        if intention == "intent_prix":
            return "Toutes nos formations sont à partir de 300 DT."

        if intention == "intent_duree":
            return "La durée standard de nos formations est de 2 à 4 mois. Pour le service de supervision de PFE, la durée est de 1 à 2 mois selon vos besoins."

        if intention == "intent_rythme":
            return "Le rythme standard est de 6 heures par semaine (4h de cours + 2h de suivi en ligne individuel). Pour la supervision, c'est jusqu'à 2 heures par semaine."

        mapping_formation = {
            "intent_web": ["Full Stack Web Development"],
            "intent_data_ia": ["Artificial Intelligence", "IA", "Business Analytics", "Business Intelligence"],
            "intent_iot": ["Internet Of Things"],
            "intent_pfe": ["Preparation Before PFE"],
            "intent_bootcamp": ["Summer Bootcamp"],
            "intent_supervision": ["Supervision and follow up"],
            "intent_mobile": []
        }

        noms_recherches = mapping_formation.get(intention, [])

        if intention == "intent_mobile":
            return "Nous n'avons pas actuellement de formation spécifique pour le développement mobile dans notre catalogue."

        if not noms_recherches:
            return None

        mask = self.df['name'].apply(lambda x: any(nom.lower() in str(x).lower() for nom in noms_recherches))
        resultats = self.df[mask]

        if resultats.empty:
            return None

        reponse = "Voici les détails de la formation :\n\n"
        for _, row in resultats.iterrows():
            reponse += f"📘 **{row['name']}**\n"
            desc_fr = self.traduire_vers_francais(str(row['description']))
            reponse += f"{desc_fr}\n"

        return reponse.strip()

    # ==========================================
    # MÉTHODE PRINCIPALE À APPELER DEPUIS L'API
    # ==========================================
    def repondre(self, user_input: str) -> str:
        langue_user = self.detecter_langue(user_input)
        question_fr = self.traduire_vers_francais(user_input)

        intention = self.detecter_intention_hybride(question_fr)

        if intention:
            reponse_fr = self.generer_reponse_structuree(question_fr, intention)

            if reponse_fr:
                return self.traduire_reponse_finale(reponse_fr, langue_user)
            else:
                return "J'ai compris le sujet, mais je ne trouve pas de service correspondant dans le fichier."
        else:
            return "Je n'ai pas de réponse pour cette question."