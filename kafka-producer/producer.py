import time
import schedule
from json import dumps
from kafka import KafkaProducer

kafka_nodes = "kafka:9092"
my_topic = "arabic_reviews"

# List of Dummy reviews

arabic_reviews = [
    "منتج رائع! لقد كان فعالًا جدًا في تلبية احتياجاتي. أوصي به بشدة.",
    "للأسف، المنتج لم يحقق توقعاتي، الجودة أقل مما كنت أتمنى.",
    "الخدمة كانت ممتازة، الفريق كان متعاونًا للغاية. سأعود بالتأكيد!",
    "الخدمة كانت بطيئة جدًا، انتظرت وقتًا طويلًا للحصول على طلبي.",
    "تجربة تسوق ممتعة جدًا، المنتجات ذات جودة عالية وسعرها مناسب.",
    "تجربتي كانت مخيبة للآمال، لم يكن هناك اهتمام من الموظفين.",
    "المطعم يقدم أطباق شهية، الأجواء رائعة، سأزورهم مرة أخرى قريبًا.",
    "الطعام كان باردًا ولم يكن بالمستوى المطلوب. لن أعود مرة أخرى.",
    "أحببت هذا الكتاب، أسلوب الكتابة رائع والمحتوى ممتع للغاية.",
    "الكتاب لم يكن مثيرًا للاهتمام، شعرت بالملل أثناء قراءته.",
    "سلسلة من الدروس المفيدة، لقد تعلمت الكثير في وقت قصير.",
    "كانت الدروس غير منظمة، ولم أستفد منها كثيرًا.",
    "منتج مذهل! لقد أحدث فرقًا كبيرًا في حياتي اليومية.",
    "سعر المنتج مرتفع جدًا مقارنة بالجودة. لا أنصح بشرائه.",
    "كان الحجز سهلاً، والموظفون محترفون جدًا.",
    "واجهت مشكلة مع الموقع الإلكتروني، كان من الصعب إتمام الشراء.",
    "تجربة استخدام الموقع كانت سهلة وسلسة. سأنصح أصدقائي بالتأكيد.",
    "التصميم لم يكن كما توقعت، شعرت بخيبة أمل بعد استلام المنتج.",
    "أحببت التصميم والألوان، المنتج يبدو رائعًا في منزلي.",
    "لم يكن الحجز واضحًا، وألغيت رحلتي بسبب عدم توفر الأماكن."
]

def send_review():
    """Sends an Arabic review to Kafka."""
    try:
        producer = KafkaProducer(bootstrap_servers=kafka_nodes, value_serializer=lambda x: dumps(x).encode('utf-8'))
        for review in arabic_reviews:
            data = {"review": review}
            print(data)
            producer.send(my_topic, value=data)
            producer.flush()
            time.sleep(1)  # small delay between sending reviews
    except Exception as e:
        print(f"Error sending data to Kafka: {e}")

if __name__ == "__main__":
    schedule.every(30).seconds.do(send_review)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
