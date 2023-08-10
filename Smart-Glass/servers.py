import requests

def select_mode():
    while True:
        print("Select a mode:")
        print("1. Face Detection")
        print("2. Object Detection")
        print("3. Image to Text")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            mode = 'face_detection'
        elif choice == '2':
            mode = 'object_detection'
        elif choice == '3':
            mode = 'image_to_text'
        elif choice == '4':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        response = requests.post('http://192.168.137.92:5000/mode_selection', data={'mode': mode})

        if response.status_code == 200:
            print("Mode selection successful")
        else:
            print("Mode selection failed")

if __name__ == '__main__':
    select_mode()
