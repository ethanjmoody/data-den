# EduCreate

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![EugeneLinkedIn][eo_linkedin-shield]][eo_linkedin-url]
[![EthanLinkedIn][em_linkedin-shield]][em_linkedin-url]
[![XinLinkedIn][ls_linkedin-shield]][ls_linkedin-url]
[![YuriLinkedIn][yk_linkedin-shield]][yk_linkedin-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">EduCreate</h3>

  <p align="center">
    Empowering the content creator within every teacher and igniting the imagination of every student
    <br />
    <a href="https://sites.google.com/view/educreate-com/home"><strong>Hear more about the project, meet the team, and try it out! »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Teachers face a daunting challenge every day.

They are expected to craft lessons that resonate with every student, yet have limited time to plan those lessons. They are asked to ensure all students learn something, yet have to juggle a diverse range of learning styles and skill levels.

Relying on a one-size-fits-all approach doesn’t work. How can they possibly facilitate an environment of learning for every student?

The EduCreate open-source app framework provides teachers with interactive and user-friendly solutions, including a Comic Generator for creating short comics and written summaries based on input text and lesson prompts, and a Lesson Planner for designing comprehensive, personalized lesson plans.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Streamlit][Streamlit.js]][Streamlit-url]
* [![Qdrant][Qdrant.js]][Qdrant-url]
* [![Langchain][Langchain.js]][Langchain-url]
* [![HuggingFace][HuggingFace.io]][Huggingface-url]
* [![Stable Diffusion][StableDiffusion.dev]][StableDiffusion-url]
* [![Anthropic][Anthropic.com]][Anthropic-url]
* [![Docker][Docker.com]][Docker-url]
* [![OpenAI][openai.com]][openai-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Hardware Requiredments
* Linux server with minimum 8 cores and 64Gb RAM 
* Single GPU with >24 Gb of VRAM


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ykinakin/educreate
   ```
3. Install docker through apt repository. Other options for installation are available at https://docs.docker.com/engine/install/ubuntu/.
   ```sh
   # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    
    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update

   # Install docker. 
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
4. Build the docker image. The Dockerfile in this repository is configured to allow Streamlit access to port 8501. 
   ```sh
   docker build -t educreate .
   ```

5. This implementation of Educreate utilizes the Anthropic Sonnet 3.5 model to generate prompts and captions. Accessing the API requires creating a user account and generating an access token. More information on this process is available at [Anthropic](https://www.anthropic.com/api). Please note that as this is not a free model, it will be necessary to purchase usage credits. 

6. Image creation is achieved through the use of the Stable Diffusion 3 model and is accessed through the Huggingface API. Use of this model is restricted to non-commerical applications (for further information see [StabilityAI](https://stability.ai/license#select_membership). It is necessary to request access to the model through HuggingFace, then generate an access token via the the web portal. Please see [HuggingFace API](https://huggingface.co/docs/hub/en/security-tokens) for the details of this process.

7. OpenAI's Whisper model is used to transcribe audio from video. Accessing the API requires creating a user account and generating an access token. More information on this process is available at [OpenAI](https://platform.openai.com/docs/quickstart). Please note that as this is also not a free model, it will be necessary to purchase usage credits. 

8. Copy these tokens into the keys.py file, replacing the text between the quotation marks with the approptriate token. 
   ```sh
   anthropic_token = "REPLACE_WITH_YOUR_ANTHROPIC_TOKEN"
   huggingface_token = "REPLACE_WITH_YOUR_HUGGINGFACE_TOKEN"
   openai_token = "REPLACE_WITH_YOUR_OPENAI_TOKEN"
   ```

7. The streamlit server can be started using the provided script. Note that, upon first running the program, the T5 and Stable Diffusion 3 models will be downloaded and cached and the RAG retrieved will be created. Depending on internet connection speed, this can take up to 30 min. Any subsequent runs should take less than 10 seconds to instantiate. 
   ```sh
   ./streamlist/start_streamlit
   ```

<!-- USAGE EXAMPLES -->
## Usage

Navigating to the web portal will present a user with the following landing page. A brief explanation of the project and links to the EduCreate website and github page are provided. 

![Landing_page](streamlit/Landing_page.png?raw=true "Landing_page")

Clicking on the "Comic Generator" will bring up the following page, in which a user is prompted to enter a lesson objective, choose a comic style and optionally provide additional source material via upload. A user is then able to both generate a short text answer that answers the lesson objective as well as a series of comic panels that also explain the lesson objective. Once generated, a user is able to save the outputs via download buttons. 

![Comic_generator](streamlit/Video_output.png?raw=true "Comic_generator")

Clicking on the "Lesson Planner" will bring up the following page, in which a user is prompted to either enter a lesson plan or accept the default. A video type and source must be specified, after which a short summary and lesson plan can be generated to support the video. This can either be used by a teacher to interact with to existing videos that were planned for classroom use by providing additional context, or can be used on in-house lectures or Zoom recordings. 

![Audio_generator](streamlit/Audio_output.png?raw=true "Audio_generator")


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Add site security (signed key) to Streamlit server. 
- [ ] Add ability to select and improve upon generated comics on a panel-by-panel basis.
- [ ] Multi-language Support
    - [ ] Spanish
    - [ ] French

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull RequestaceSmile&logoColor=white
[HuggingFace-url]: https://huggingface.co/

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [othneildrew's Awesome Readme Template](https://github.com/othneildrew/Best-README-Template)
* [React Icons](https://react-icons.github.io/react-icons/search)
* [Official EduCreate GitHub Repo](https://github.com/ykinakin/educreate/tree/main)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/ykinakin/educreate/issues
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/ykinakin/educreate/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt

[eo_linkedin-shield]: https://img.shields.io/badge/-Eugene_LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[eo_linkedin-url]: https://www.linkedin.com/in/eugene-oon-soo-kai-998453b/
[em_linkedin-shield]: https://img.shields.io/badge/-Ethan_LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[em_linkedin-url]: https://www.linkedin.com/in/ethanjmoody/
[ls_linkedin-shield]: https://img.shields.io/badge/-Xin_LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[ls_linkedin-url]: https://www.linkedin.com/in/xinsong96/
[yk_linkedin-shield]: https://img.shields.io/badge/-Yuri_LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[yk_linkedin-url]: https://www.linkedin.com/in/ykinakin/

[product-screenshot]: images/screenshot.png
[Streamlit.js]: https://img.shields.io/badge/Streamlit-000000?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/
[Qdrant.js]: https://img.shields.io/badge/Qdrant-20232A?style=for-the-badge&logoColor=61DAFB
[Qdrant-url]: https://qdrant.tech/
[Langchain.js]: https://img.shields.io/badge/Langchain-35495E?style=for-the-badge&logo=&logoColor=4FC08D
[Langchain-url]: https://www.langchain.com/
[Huggingface.io]: https://img.shields.io/badge/HuggingFace-DD0031?style=for-the-badge&logo=FaceSmile&logoColor=white
[HuggingFace-url]: https://huggingface.co/
[StableDiffusion.dev]: https://img.shields.io/badge/Stable_Diffusion_3-4A4A55?style=for-the-badge&logoColor=FF3E00
[StableDiffusion-url]: https://stability.ai/news/stable-diffusion-3
[Anthropic.com]: https://img.shields.io/badge/Anthropic-FF2D20?style=for-the-badge&logo=anthropic&logoColor=white
[Anthropic-url]: https://www.anthropic.com/
[Docker.com]: https://img.shields.io/badge/Docker-blue?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[openai.com]: https://img.shields.io/badge/OpenAI-purple?style=for-the-badge&logo=openai&logoColor=white
[openai-url]: https://openai.com/
