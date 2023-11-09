import os
from dotenv import load_dotenv

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

#from twit import tweeter
from tweety import Twitter

from requests_oauthlib import OAuth1Session
import os

from dotenv import load_dotenv
import tweepy

import streamlit as st

load_dotenv()


template = """
% INSTRUCTIONS
    - Vous êtes un Bot IA très doué pour répondre à des tweets en imitant une personnalité.
    - Votre objectif est d'imiter la réponse de la personnalité décrite ci-dessous au tweet.
    - Réponds avec une approche scientifique lié à la psychologie ou science du cerveau.
    - L'objectif est de donner l'avis de la personnalité décrite ci-dessous si elle avait lu le tweet.
    - N'utilise pas d'expressions comme "n'est-ce pas ?".
    - Parle au moins une fois à la première personne du singulier.
    - Ne dépassez pas les instructions de personnalité ci-dessous.
    - Un tweet ne dépasse pas 280 caractères.
    - N'utilise pas de hashtags.



% Description de personnalité
Comportement social :Tu es un individu charismatique et sociable. Tu te comportes comme le scientifique cool. Tu es humble et ne dis jamais que tu es un expert ou un scientifique.
Traits émotionnels : Tu es calme et stoïque, affichant un comportement posé, ce qui te vaut une réputation de tranquillité et de sérénité.
Adaptabilité : Tu es ouvert d'esprit et flexible.
Humour : Tu as une réputation  liée à ton sérieux mais tu sais quelques fois avoir un sens de l'humour.
Ton : Le ton est positif, encourageant, et introspectif. Le langage est familier, jeune mais scientifique.

% TWEETS
    {info}
    
"""

prompt = PromptTemplate(
    input_variables=["info"], template=template
)

openai_api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key, model='gpt-4-1106-preview')
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    
)


def tweeter():
    # Load environment variables
    load_dotenv()
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    # Assuming you've added your access token and secret to the .env file
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
    bearer_token = os.environ.get("bearer_token")

    client = tweepy.Client(bearer_token=bearer_token,
                        consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret)
    
    return client

  
twitapi = tweeter()

def tweetertweet(tweet, id):
    twitapi = tweeter()
    #tweets = thread.split("\n\n")
    #check each tweet is under 280 chars
    #for i in range(len(tweets)):
    if len(tweet) > 280:
            prompt = f"Raccourci ce tweet pour qu'il soit en dessous de 280 caractères : {tweet}"
            tweet = llm.predict(prompt)[:280]
    #give some spacing between sentances
    tweet = tweet.replace('. ', '.\n\n')

    #for tweet in tweets:
    #tweet = tweet.replace('**', '')

    #response = twitapi.create_tweet(text=tweets[0])
    #id = response.data['id']
    #tweets.pop(0)
    #for i in tweets:
    #print("tweeting: " + tweet)
    cok="cest ok"
    reptweet = twitapi.create_tweet(text=tweet, 
                                    in_reply_to_tweet_id=id, 
                                    )
    return cok


def read_tweet_url(url) :
    app = Twitter("session")
    app.sign_in("cabinetdesidees", "testapi1319")
    tweet = app.tweet_detail(url)
    return tweet

def post_tweet(tweat, id) :
    return "Cest poste... miam !"

def main():
    
    # Set page title and icon
    st.set_page_config(page_title="FRAMATOME research agent Thread", page_icon=":bird:")

    # Display header 
    st.header("FRAMATOME research agent :bird:")
    
    # Get user's research goal input
    urld = st.text_input("adresse du tweet")

    # Initialize result and thread state if needed
    #if not hasattr(st.session_state, 'tweat'):
        #st.session_state.tweat = None

    # Do research if query entered and no prior result
    if urld : #and (st.session_state.tweat is None):
        q=read_tweet_url(urld)
        query=q.text
        greatid=q.id
        
        # Generate thread from result
        tweat=llm_chain.predict(info=query)
        st.session_state.tweat = tweat

        # Display generated thread and result if available
        if st.session_state.tweat:
            st.markdown(st.session_state.tweat)
        
            # Allow tweeting thread
    
            if st.button("Tweeeeeet"):
                # Tweet thread
                #tweetertweet(tweat,greatid)
                etatdut=post_tweet(tweat,greatid)
                st.markdown(etatdut)
                #st.session_state.etatdut = tweetertweet(tweat,greatid)
            
 

if __name__ == '__main__':
    main()
