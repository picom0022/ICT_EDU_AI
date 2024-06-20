import os
import csv
import json

# JSON 파일들이 있는 디렉토리 경로
json_dir = 'D:/Final/Dataset/tt'

# CSV 파일 경로
csv_file_path = 'D:/Final/Dataset/output.csv'
print("시작")
# CSV 파일 생성 및 헤더 작성
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Occupation', 'Gender', 'AgeRange', 'Experience', 'Question'])

    # 디렉토리 내의 모든 JSON 파일에 대해 처리
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            json_file = os.path.join(json_dir, filename)
            try:
                with open(json_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    # 데이터 추출
                    occupation = data['dataSet']['info']['occupation']
                    gender = data['dataSet']['info']['gender']
                    ageRange = data['dataSet']['info']['ageRange']
                    experience = data['dataSet']['info']['experience']
                    question = data['dataSet']['question']['raw']['text']
                    
                    # CSV 파일에 데이터 작성
                    writer.writerow([occupation, gender, ageRange, experience, question])
                    print(f"Processed file: {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

print("CSV 파일이 성공적으로 생성되었습니다.")