import os
from utils import parse_chat_log, summarize_chat, process_folder

def main():
    file_or_folder = 'sample_chats'  # Can be a folder or a specific file
    use_tfidf = True  # Change to False for frequency-based keywords

    if os.path.isfile(file_or_folder) and file_or_folder.endswith('.txt'):
        messages = parse_chat_log(file_or_folder)
        summary = summarize_chat(messages, use_tfidf=use_tfidf)
        print(f"\n==== Summary for {file_or_folder} ====")
        print(summary)
    elif os.path.isdir(file_or_folder):
        summaries = process_folder(file_or_folder, use_tfidf=use_tfidf)
        for filename, summary in summaries:
            print(f"\n==== Summary for {filename} ====")
            print(summary)
    else:
        print("Invalid input path. Please provide a valid .txt file or directory.")

if __name__ == "__main__":
    main()
