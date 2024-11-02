# MagicUp (DUKE AI Hackathon 2024)

Member: Jiechen Li, Jeff Luo, Hiep Nguyen

## What it does
MagicUp transforms makeup applications into an effortless, personalized innovative “magic mirror” experience. The mirror looks and functions as a regular mirror until activated by a hot word. Once the user says the hot word, the mirror transforms: a display screen behind the mirror lights up, and the AI takes a photo of the user’s bare face. The user can then specify their desired makeup style, and a customized open-source makeup model and OpenAI APIs generate a virtual version of their face with that makeup applied.
The virtual makeup is then displayed on the screen behind the half-silvered mirror, allowing the user to see both their real face and the AI-suggested makeup overlay at once. This synchronized display enables the user to “trace” the AI-applied makeup onto their own face, effortlessly following each feature for precise, professional results.

## How we built it
We combined hardware and advanced AI software for a seamless user experience. The setup uses Orange Pi 5 and an acrylic half-silvered mirror as the core hardware, supporting a display screen, a speaker, and a microphone as well as AI processing. For the software, we used the Snowboy locally to detect hot words. Then we customized an open-source face parsing model and integrated OpenAI APIs to generate realistic, tailored looks based on user input. When the hot word is spoken, the system activates, takes a photo of the user’s bare face, and applies the selected makeup style digitally. This blend of hardware and software brings personalized makeup guidance to users without the need for extensive tutorials or time-consuming practice—delivering an experience that’s intuitive, engaging, and tailored to individual preferences.

## Instruction:

### Set up OpenAI API key:
```cmd
export OPENAI_API_KEY=your key
```

### Install requirements
```cmd
pip install -r requirements.txt
```

### How to use the program
- Start the main program, press the button appearing on the app to record your request:
```cmd
python callRequest.py
```
- Change your image file in `app.py` in `main` function
- By default save your image in `face-makeup` folder with `image.jpeg` name.

### Specification:
- In default setting, the program create a make up layer with modified the hair, upper and lower lips, left and right eyes. Further attributes can be changed in `makeup.py` file in `makeup` function, `parts` variable.
- The face/skin can be segmented but without nose, from the currect model architecture and weight, it is hard to detect nose, thus, only change face/skin color may not be reasonable. 
- Prompt: "User request +  Generate a json file of hair, upper lip, lower lip, left eye, and right eye color for the requested makeup in this format: [[r, g, b], [r, g, b],[r, g, b], [r, g, b], [r, g, b]]. Just generate the array only without any text." 


## References:
- Facial Parsing: https://github.com/zllrunning/face-parsing.PyTorch
