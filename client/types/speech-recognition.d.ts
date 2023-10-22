declare global {
  interface Window {
    SpeechRecognition: typeof SpeechRecognition;
    webkitSpeechRecognition: typeof SpeechRecognition;
  }
}

export type SpeechRecognitionEvent = Event & {
  resultIndex: number;
  results: {
    [index: number]: {
      [index: number]: {
        transcript: string;
        language: string;
      };
    };
  };
};
