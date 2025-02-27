import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="AI-Travel Planner",layout="centered",page_icon="✈️")
st.title("  AI-Travel Planner")
st.write("Enter details to get estimated travel costs for various travel modes(including cab, train, bus, and flights).")


source = st.text_input("📍 Source:")
destination = st.text_input("📍 Destination:")


if st.button("Get Travel plan"):
    if source and destination:
        with st.spinner("Compiling all travel options ...."):
            chat_template = ChatPromptTemplate(messages=[
                ("system", """
                You are an AI-powered travel assistant designed to help users find the best travel options between a given source and destination.
                Upon receiving the source and destination, generate a list of travel options, including cab, bus, train, and flight choices. 
                For each option, provide the following details: mode of transport, estimated price, travel time, and relevant details like stops or transfers in minimum 50 words.
                Present the information in a clear format for easy comparison. 
                Focus on accuracy, cost-effectiveness, and convenience, ensuring that the user can make an informed decision based on their preferences.
                Keep the output concise, ensuring clarity and ease of understanding.
                Do not include and ouput in tablar format, keep all output as strings. 
                Recommend best possible travel mode and best time to travel at the end.
                """),
                ("human", "Find travel options from {source} to {destination} along with estimated costs.")
            ])
            
            chat_model = ChatGoogleGenerativeAI(api_key="AIzaSyB878TajR7UN2Lc_S4CJP3mJsw4FZVJXf8", model="gemini-2.0-flash-exp")
            parser = StrOutputParser()
            
            
            chain = chat_template | chat_model | parser
            
            
            raw_input = {"source": source, "destination": destination}
            response = chain.invoke(raw_input)
            
            st.success("Estimated Travel Options and Costs:",icon="✅")
            travel_modes = response.split("\n")  
            for mode in travel_modes:
                st.markdown(mode)
    else:
        st.error("Error!!! Please enter both source and destination")
