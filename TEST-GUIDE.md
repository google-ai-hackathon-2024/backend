## How to test 🎙️MinuteTaker AI🚀

See the product details ([slide](https://github.com/google-ai-hackathon-2024/backend/blob/5c7b1127791ca0535941a6aec4c737344af81c97/minutetaker-ai.pdf))!

1. **Ensure the Frontend and the Backend are running.**

    If you follow the instructions in each README, you can check whether it is running properly or not.

    - [Frontend](https://github.com/google-ai-hackathon-2024/frontend?tab=readme-ov-file#how-to-run-frontend): `http://localhost:3000`
    - [Backend](https://github.com/google-ai-hackathon-2024/backend#how-to-run-backend): `http://localhost:5000`

2. **Upload the audio file or Record by yourself.** 

    For the test efficiency, we recommend you use the given sample audio file in the Backend repository.

    - Type 1. Business meeting: [biz-result-oup-team-meeting_16k.wav](https://github.com/google-ai-hackathon-2024/backend/blob/main/dataset/biz-meeting/biz-result-oup-team-meeting_16k.wav)
        - The number of speakers: 3
        - Description: It is a team meeting conversation.
    - Type 2. Debate: [2012-first-debate-biden-ryan_16k.wav](https://github.com/google-ai-hackathon-2024/backend/blob/main/dataset/debating/2012-first-debate-biden-ryan_16k.wav)
        - The number of speakers: 3
        - Description: It is the US vice presidential debate in 2012 between Joe Biden and Paul Ryan.
    - Type 3. Interview: [Ken_Robinson_16k.wav](https://github.com/google-ai-hackathon-2024/backend/blob/main/dataset/interview/Ken_Robinson_16k.wav)
        - The number of speakers: 2
        - Description: It is a TED interview with Ken Robinson. It is hosted by Chris Anderson.
    - Type 4. Monologue: [DJ_221_ban-gambling_con_opening_YBA_16k.wav](https://github.com/google-ai-hackathon-2024/backend/blob/main/dataset/monologue/DJ_221_ban-gambling_con_opening_YBA_16k.wav)
        - The number of speakers: 1
        - Description: It is a monologue talking about the topic of 'banning gambling'.

3. **Set information about the conversation.**

    You can find the corresponding information in the sample audio file above.

    - The number of speakers
    - Short description to help you set the conversation type, title, and speaker name.

    ***NOTE:*** This step will take few minutes to make a transcribtion for the audio file.
    
    ref. 5min audio: ~2min to be processed

4. **Explore the result page.**

    - Click 'Summary' and 'Transcript' to see the result.
    - Click the 'Download' button for each.
    - Ask questions about the conversation.

        e.g.
        
        What are the names of the conversation participants?

        What is the topic of this conversation? Tell me shortly.

        What is the meaning of 'TED' in this conversation?

        ...

5. **Share the result page with other users.**

    - Click the 'Share Chat' button on the upper right.
    - Open another browser and paste the shared link.
    - Start chatting in multiple browsers.

