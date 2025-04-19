from gtts import gTTS
import random
import os
from playsound import playsound

questions = [
    {
        "dialogue": "여자: 민수 씨 이번 주 모임 장소가 바뀌었대요\n남자: 그래요? 어디로 바뀌었어요?\n여자:",
        "options": [
            "장소를 다시 말해 주세요", 
            "다음 모임은 안 갈 거예요", 
            "이번 주에 만나면 좋겠어요", 
            "정문 옆에 있는 식당이에요"
        ],
        "correct_answer": 4
    },
    {
        "dialogue": "남자: 기차표 알아봤는데 금요일 오후 표는 없는 것 같아\n여자: 그럼 토요일 아침 어때?",
        "options": [
            "아침 일찍 기차를 탔어", 
            "표가 없어서 아직 못 갔어", 
            "표가 있는지 한번 알아볼게", 
            "금요일 오후 표는 취소하자"
        ],
        "correct_answer": 3
    },
    {
        "dialogue": "여자: 내일 발표만 끝나면 이제 이번 학기도 끝나네요\n남자: 그러게요 수미 씨 방학 계획은 세웠어요?",
        "options": [
            "발표는 늘 어렵지요", 
            "계획부터 세워 보세요", 
            "외국어 공부를 좀 할까 해요", 
            "학기가 시작되면 많이 바빠요"
        ],
        "correct_answer": 3
    },
    {
        "dialogue": "남자: 이번에 새로 시작한 드라마 말이야 진짜 재미있더라\n여자: 아 그 시골에서 할머니랑 사는 아이 이야기?",
        "options": [
            "응 시골에서 산 적이 있어", 
            "아니 너무 지루해서 졸았어", 
            "아니 드라마 볼 시간이 없었어", 
            "응 두 사람 보면서 한참 웃었어"
        ],
        "correct_answer": 4
    },
    {
        "dialogue": "여자: 오늘 회의가 오후 3시였죠?\n남자: 아니에요 시간이 조금 바뀌었어요",
        "options": [
            "그럼 몇 시에 시작해요?", 
            "회의실은 어디예요?", 
            "다음 주는 괜찮을까요?", 
            "저는 오늘 바빠요"
        ],
        "correct_answer": 1
    },
        {
        "dialogue": "여자: 오늘 날씨 정말 좋네요\n남자: 네, 햇볕도 좋고 바람도 선선해요\n여자:",
        "options": [
            "그럼 저녁에 산책할까요?", 
            "그럴 때는 집에서 쉬는 게 좋아요", 
            "이럴 때는 영화 보러 가는 게 좋아요", 
            "다음 주에 날씨가 어떨까요?"
        ],
        "correct_answer": 1
    },
    {
        "dialogue": "남자: 이번 주말에 친구랑 여행 가기로 했어요\n여자: 어디로 가는데요?",
        "options": [
            "바다 쪽으로 가요", 
            "산으로 가요", 
            "박물관에 가요", 
            "공원에서 놀 거예요"
        ],
        "correct_answer": 1
    },
    {
        "dialogue": "여자: 어제 본 영화 정말 감동적이었어요\n남자: 어떤 영화였어요?",
        "options": [
            "사랑 이야기 영화였어요", 
            "액션 영화였어요", 
            "감정이 복잡한 영화였어요", 
            "공포 영화였어요"
        ],
        "correct_answer": 1
    },
    {
        "dialogue": "남자: 새로 오픈한 식당 가봤어요?\n여자: 아직 못 갔어요. 그런데 평이 좋다고 들었어요.",
        "options": [
            "그럼 이번 주말에 같이 가요", 
            "그럼 나도 가봐야겠어요", 
            "그 식당은 너무 비쌀 것 같아요", 
            "그 식당은 너무 멀어요"
        ],
        "correct_answer": 1
    },
    {
        "dialogue": "여자: 지금 너무 배고파요\n남자: 뭐 먹고 싶어요?",
        "options": [
            "한식 먹고 싶어요", 
            "중식 먹고 싶어요", 
            "일식 먹고 싶어요", 
            "패스트푸드 먹고 싶어요"
        ],
        "correct_answer": 1
    },
    {
        "dialogue": "남자: 내일 날씨는 비가 올 것 같아요\n여자: 그럼 우산을 챙겨야겠네요",
        "options": [
            "네, 우산 안 챙기면 안 되겠어요", 
            "괜찮아요, 비는 잠깐 올 거예요", 
            "우산 없이도 충분히 괜찮아요", 
            "그냥 집에 있을 거예요"
        ],
        "correct_answer": 1
    },
    {
        "dialogue": "여자: 지난번에 새로 개봉한 영화 봤어요?\n남자: 네, 정말 재미있었어요. 추천해요.",
        "options": [
            "그 영화는 너무 지루했어요", 
            "그 영화는 너무 감동적이었어요", 
            "그 영화는 볼 가치가 없어요", 
            "그 영화는 예고편보다 나았어요"
        ],
        "correct_answer": 2
    },
    {
        "dialogue": "남자: 저는 운동을 시작하려고 해요\n여자: 운동을 시작하는 게 정말 좋은 선택이에요!",
        "options": [
            "그럼 어떤 운동을 시작할 거예요?", 
            "운동을 시작할 시간이 없어요", 
            "운동은 별로 하고 싶지 않아요", 
            "운동을 시작하기엔 너무 늦었어요"
        ],
        "correct_answer": 1
    },
    {
        "dialogue": "여자: 이 식당은 분위기가 정말 좋아요\n남자: 그렇죠. 음식도 맛있고, 가격도 괜찮아요.",
        "options": [
            "가격이 좀 비싸요", 
            "음식이 정말 맛없었어요", 
            "다음에 또 가고 싶어요", 
            "그냥 그런 식당이에요"
        ],
        "correct_answer": 3
    },
    {
        "dialogue": "남자: 오늘은 정말 바쁜 하루였어요\n여자: 그렇죠, 일이 많았어요?",
        "options": [
            "네, 일을 끝내고 좀 쉴 거예요", 
            "아니요, 그냥 하루가 빨리 지나갔어요", 
            "네, 내일도 바쁠 것 같아요", 
            "아니요, 그냥 아무것도 안 했어요"
        ],
        "correct_answer": 1
    }
]


def read_dialogue(text):

    tts = gTTS(text=text, lang='ko', slow=False)
    

    tts.save("output_audio.mp3")
    print("Audio saved successfully.")
    

    playsound("output_audio.mp3")


def display_question(question):
    print("Dialogue: " + question["dialogue"])
    print("Options:")
    for i, option in enumerate(question["options"], start=1):
        print(f"{i}. {option}")
    #print(f"Correct Answer: Option {question['correct_answer']}")


    read_dialogue(question["dialogue"])


def check_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        print("✅ Correct!")
        return True
    else:
        print(f"❌ Incorrect. The correct answer is Option {correct_answer}.")
        return False


def main():

    selected_question = random.choice(questions)
    

    display_question(selected_question)
    

    try:
        user_answer = int(input("Enter your answer (1, 2, 3, or 4): "))
        if user_answer < 1 or user_answer > 4:
            print("⚠️ Please enter a number between 1 and 4.")
        else:

            check_answer(user_answer, selected_question["correct_answer"])
    
    except ValueError:
        print("⚠️ Please enter a valid number between 1 and 4.")


if __name__ == "__main__":
    main()