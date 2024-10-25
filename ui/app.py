import streamlit as st
import time
import psycopg2
from psycopg2 import OperationalError
import logging
from langchain_cohere import ChatCohere 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the connection parameters
DB_HOST = os.environ["DB_HOST"] 
DB_NAME = os.environ["DB_NAME"] 
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"] 
DB_PORT = os.environ["DB_PORT"]

# Initialize Cohere LLM
llm = ChatCohere(
    model="command-r-plus",
    temperature=0.0,
    cohere_api_key=os.environ['COHERE_API_KEY']
)

def fetch_data():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM arabic_reviews ORDER BY id DESC LIMIT 100")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except OperationalError as e:
        st.error(f"Error connecting to the database: {e}")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None
def get_insights(reviews, sentiment):
    prompt = PromptTemplate(
        input_variables=["reviews", "sentiment"],
        template="""
        أنت خبير رائد في تحليل المشاعر والتعليقات. 
        لديك القدرة على استخلاص الأفكار الهامة وتقديم رؤى معمقة. 
        يرجى تحليل التعليقات التالية التي تعكس مشاعر {sentiment} باللغة العربية. 
        قدِّم ملخصًا شاملًا يتضمن النقاط الرئيسية التي تعكس المشاعر السائدة، 
        وتسلط الضوء على الموضوعات الشائعة والاتجاهات الملحوظة. 
        استند إلى الأسلوب واللغة المستخدمة في التعليقات، وامنح توصيات أو أفكار لتحسين التجربة المستقبلية.

        التعليقات:
        {reviews}

        ملخص ورؤى:
        """
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.invoke({"reviews": "\n".join(reviews), "sentiment": sentiment})

def main():
    st.set_page_config(page_title="تحليل آراء المستفيدين", page_icon="📊", layout="wide")
    st.title("تحليل آراء المستفيدين")
    st.write("عرض وتحليل آراء المستفيدين في الوقت الفعلي")

    # Create three columns
    col1, col2, col3 = st.columns(3)

    # Counters for positive and negative reviews
    positive_count = 0
    negative_count = 0
    positive_reviews = []
    negative_reviews = []

    while True:
        data = fetch_data()
        if data:
            # Clear existing content
            col1.empty()
            col2.empty()
            col3.empty()

            # Display reviews
            with col1:
                st.subheader("آخر التعليقات")
                for row in data:
                    review = row[1]
                    sentiment = row[2]
                    if sentiment == "ايجابي":
                        st.success(f"{review} - {sentiment}")
                        positive_count += 1
                        positive_reviews.append(review)
                    else:
                        st.error(f"{review} - {sentiment}")
                        negative_count += 1
                        negative_reviews.append(review)

            # Display statistics
            with col2:
                st.subheader("إحصائيات")
                total_reviews = positive_count + negative_count
                if total_reviews > 0:
                    positive_percentage = (positive_count / total_reviews) * 100
                    negative_percentage = (negative_count / total_reviews) * 100
                    st.metric("إجمالي التعليقات", total_reviews)
                    st.metric("التعليقات الإيجابية", f"{positive_count} ({positive_percentage:.1f}%)")
                    st.metric("التعليقات السلبية", f"{negative_count} ({negative_percentage:.1f}%)")
                    
                    st.bar_chart({"إيجابي": positive_count, "سلبي": negative_count})
                else:
                    st.write("لا توجد تعليقات بعد")

            # Display insights
            with col3:
                st.subheader("التحليل والرؤى")
                if positive_reviews:
                    st.write("### تحليل التعليقات الإيجابية")
                    with st.spinner("جاري تحليل التعليقات الإيجابية..."):
                        positive_insights = get_insights(positive_reviews[-10:], "إيجابي")
                    st.write(positive_insights['text'])

                if negative_reviews:
                    st.write("### تحليل التعليقات السلبية")
                    with st.spinner("جاري تحليل التعليقات السلبية..."):
                        negative_insights = get_insights(negative_reviews[-10:], "سلبي")
                    st.write(negative_insights['text'])

        else:
            st.write("لا توجد بيانات")
        
        time.sleep(60)  
        st.rerun()

if __name__ == "__main__":
    main()
