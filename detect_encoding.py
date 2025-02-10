import chardet

# استبدل "temperature_sample.csv" بمسار ملف CSV الخاص بك
with open("temperature_sample.csv", "rb") as f:
    result = chardet.detect(f.read())
    print(result)