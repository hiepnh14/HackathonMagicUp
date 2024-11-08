# MagicUp (DUKE AI Hackathon 2024)

Member: Jiechen Li, Jeff Luo, Hiep Nguyen


## Links

- [Demo Video](https://youtu.be/bLvHS5BqWbs) 

- [Slides](https://docs.google.com/presentation/d/18BfE0v86iz50tZHiundPFp1a1IkfIapSqml-f-MqXQI/edit?usp=sharing) 

## Inspiration

The beauty industry is booming, with U.S. consumers spending $89.7 billion annually and global revenue projected to reach $688.89 billion by 2028 ([Statista.com](https://www.statista.com/outlook/cmo/beauty-personal-care/worldwide)). Consumers increasingly seek personalized makeup experiences, with 75% responding positively to tailored recommendations. Social media also plays a major role, influencing 42% of buyers aged 18-24. Also, 67% of beauty shoppers say they turn to influencers to discover new products. ([Swnsdigital.com](https://swnsdigital.com/us/2017/06/women-spend-a-quarter-of-a-million-dollars-on-their-appearance-in-a-lifetime/), [Terakeet](https://terakeet.com/blog/beauty-industry/)).
While makeup coaches and influencers share endless techniques, keeping up with trends, adapting to different styles, and finding the right look can be overwhelming and time-consuming for individuals. Our inspiration is to simplify this process, giving users a tool that leverages smart hardware and AI to provide customized, easy-to-follow makeup guidance tailored to their unique needs.

---


## What it does
MagicUp transforms makeup applications into an effortless, personalized innovative “magic mirror” experience. The mirror looks and functions as a regular mirror until activated by a hot word. After a display screen behind the mirror lights up, then the user says the hot word, the mirror transforms: detects, and fits the user’s face into a red rectangle, and then the AI takes a photo of the user’s bare face. The user can then specify their desired makeup style, and a customized open-source face parsing model and OpenAI APIs generate a virtual version of their face with that makeup applied.
The virtual makeup is then displayed on the screen behind the half-silvered mirror, allowing the user to see both their real face and the AI-suggested makeup overlay at once. This synchronized display enables the user to “trace” the AI-applied makeup onto their own face, effortlessly following each feature for precise, professional results.


---



## How we built it
We combined hardware and advanced AI software for a seamless user experience. The setup uses Orange Pi 5 and an acrylic half-silvered mirror as the core hardware, supporting a display screen and a microphone as well as AI processing. For the software, we used the Snowboy API locally to detect hot words. Then we customized an open-source face parsing model and integrated OpenAI and Google APIs to generate realistic, tailored looks based on user input. When the hot word is spoken, the system activates, takes a photo of the user’s bare face, and applies the selected makeup style digitally. This blend of hardware and software brings personalized makeup guidance to users without the need for extensive tutorials or time-consuming practice—delivering an experience that’s intuitive, engaging, and tailored to individual preferences.


---

## Challenges we ran into

For **hardware**, we encountered significant challenges in adapting various external devices and sensors, including the camera, microphone, speaker, and screen. One major issue was the camera driver, which was initially broken and prevented proper functionality. By carefully studying the hardware documentation, we identified and temporarily fixed the driver bug, allowing us to capture images for testing. However, after a system reboot to relocate for video recording, the setup failed again, revealing the fragility of our code under real-world conditions. This instability was eventually traced to an unstable power supply on the Orange Pi under high load. With only four hours before submission, we stabilized the system by securing a more consistent power source, allowing us to complete a successful demonstration.

We also faced issues with the Bluetooth speaker, which could not be set as the default audio device. To work around this, we implemented a solution to display AI-generated instructions as text on the screen instead of using audio playback. While this preserved core functionality, the setup remained sensitive to restarts. Nevertheless, we maintained reliable functionality throughout our final tests.

On the **software** side, package dependency conflicts required extensive debugging, and while our face parsing model ran smoothly on a PC, running it on our hardware was another challenge due to limited processing power. This affected the display quality, as the hardware struggled to keep up with real-time rendering. Despite these constraints, we successfully optimized the model’s performance on the Orange Pi, allowing us to deliver a functional prototype. These experiences underscored the complexities of adapting high-performance software to constrained hardware environments, ultimately pushing us to find creative solutions that enabled our final success.



---

## Accomplishments that we're proud of

We’re proud to have seen our vision for MagicUp come to life during this hackathon, transforming the concept of a “magic mirror” into a functional, innovative tool. Through effective collaboration, we achieved integration of hardware and software components, and we successfully ran the system during testing. Our custom-built system enabled MagicUp to capture a raw photo from the hardware camera, which was processed through our makeup model with enhancements from OpenAI and Google APIs to deliver personalized, realistic makeup guidance.
One particular challenge involved the Bluetooth speaker, which we couldn’t set as the default audio device. After troubleshooting without success, we adapted our approach by switching to text-based instructions displayed on the screen. This allowed us to maintain functionality in the short term. We also encountered an issue with system reboots when moving to a quieter area for video recording. After extensive troubleshooting, we identified the cause—unstable power supply on the Orange Pi under high load—and resolved it just four hours before submission. This last-minute fix stabilized the setup and allowed us to successfully demonstrate the final product.
Overcoming these technical barriers and coordinating complex interactions between hardware and AI-driven software was a rewarding achievement. This experience not only showcased our technical skills but also underscored the collaborative spirit and innovative thinking that made MagicUp possible.


---

## What we learned

- **Effective Team Collaboration**: This project reinforced the importance of clear communication and teamwork, especially when integrating hardware and software components. Each team member’s role was crucial in overcoming the technical obstacles, allowing us to build a fully functional prototype.

- **Technical Problem-Solving**: Adapting various external devices taught us valuable troubleshooting skills. For example, we resolved camera driver issues and handled package conflicts. Our final challenge with power stability on the Orange Pi highlighted the importance of power management under high-load conditions for a robust system.

- **Adaptability and Quick Problem-Solving**: When the Bluetooth speaker issue prevented audio playback, we quickly adapted by switching to text-based instructions. This workaround allowed us to maintain functionality, and solving the power stability issue further reinforced our adaptability under pressure.

- **Hardware-Software Coordination**: The most challenging part of the project was achieving coordination between hardware and software. Our face parsing model ran smoothly on a computer but required adaptation on the Orange Pi due to performance limitations. This experience highlighted the complexities of developing real-time applications on hardware with limited processing power.

- **Leveraging Open Source and APIs**: Customizing open-source models and integrating APIs like Snowboy and OpenAI expanded our understanding of working with external tools. These resources accelerated development but required thoughtful adaptation for our hardware setup.

- **User-Centric Design**: MagicUp’s design process deepened our understanding of creating intuitive, user-centered applications. We prioritized accessibility and ease of use, even under technical constraints, which was a valuable lesson in balancing functionality with user experience.

- **Time Management and Adaptability**: The hackathon’s time constraints taught us to adapt quickly, stay focused, and find creative solutions. The last-minute resolution of the power supply issue underscored the need for robust solutions, preparation, and adaptability under pressure.


---


## What's next for MagicUp

- **Hardware Optimization**:
  - Restructure code with C++ to improve processing speed.
  - Integrate built-in hardware (WiFi, speaker, camera) and reduce circuit size for increased portability and diverse applications.
  - Enhance power efficiency to extend usage in various settings.

- **Software Enhancements**:
  - Upgrade the GUI for better responsiveness and user experience.
  - Improve algorithm accuracy and efficiency, allowing for more customized recommendations.
  - Develop a newer, more advanced makeup model to replace the current five-year-old version, or build our own environment and system to eliminate the need for adaptation and compromise.

- **Real-world Applications**:
  - **Automotive**: Integrate MagicUp into car sun visor mirrors to adapt users’ convenience, and on-the-go use in both driver and passenger seats.
  - **Cosmetic Retail**: Deploy MagicUp in makeup stores to boost customer confidence in new products, supporting increased sales.
  - **Makeup Influencers**: Enable influencers to teach efficient makeup techniques with MagicUp, fostering community engagement and promoting the tool, helping influencers retain followers while popularizing MagicUp.




## Instruction

### Set up OpenAI API key
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

### Specification
- In default setting, the program create a make up layer with modified the hair, upper and lower lips, left and right eyes. Further attributes can be changed in `makeup.py` file in `makeup` function, `parts` variable.
- The face/skin can be segmented but without nose, from the currect model architecture and weight, it is hard to detect nose, thus, only change face/skin color may not be reasonable. 
- Prompt: "User request +  Generate a json file of hair, upper lip, lower lip, left eye, and right eye color for the requested makeup in this format: [[r, g, b], [r, g, b],[r, g, b], [r, g, b], [r, g, b]]. Just generate the array only without any text." 


## References
- Facial Parsing: https://github.com/zllrunning/face-parsing.PyTorch
