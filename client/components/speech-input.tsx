"use client";
import React, { useRef, useState, useEffect, useCallback } from "react";
import { Textarea } from "./ui/textarea"; // Assuming you have a Textarea component
import { Button } from "./ui/button";
import { Icons } from "./ui/icons";

interface SpeechInputProps {
  language: string;
}

export default function SpeechInput({ language }: SpeechInputProps) {
  const [transcript, setTranscript] = useState<string>("");
  const [isListening, setIsListening] = useState<boolean>(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const lastResultIndexRef = useRef<number>(0);

  const startRecognition = useCallback(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.lang = language; // Set the language

    // Enable continuous recognition and interim results for real-time feedback
    recognition.continuous = true;
    // recognition.interimResults = true;

    // recognition.onresult = (event) => {
    //   const current = event.resultIndex;
    //   const transcriptSegment = event.results[current][0].transcript;
    //   setTranscript(
    //     (prevTranscript) => prevTranscript + " " + transcriptSegment
    //   );
    // };
    recognition.onresult = (event) => {
      let interimTranscript = "";
      let finalTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcriptSegment = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcriptSegment;
        } else {
          interimTranscript += transcriptSegment;
        }
      }

      setTranscript((prevTranscript) => prevTranscript + finalTranscript);
    };

    recognition.start();
  }, [language]);

  const stopRecognition = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }
  }, []);

  useEffect(() => {
    if (isListening) {
      startRecognition();
    } else {
      stopRecognition();
    }
    return () => {
      stopRecognition();
    };
  }, [language, isListening, startRecognition, stopRecognition]);

  return (
    <div>
      <Textarea
        className="h-[50px] relative w-full max-w-screen-md  border border-gray-200 bg-white px-4 pb-2  shadow-lg sm:pb-3 sm:pt-4 items-center max-h-[200px] max pt-3 resize-none rounded-xl"
        placeholder="Type your message here."
        value={transcript}
        autoFocus
        onChange={(e) => setTranscript(e.target.value)}
      />
      {!isListening ? (
        <Button
          className="absolute top-6 right-1 "
          onClick={() => setIsListening(!isListening)}
          variant="ghost"
        >
          <Icons.mic className="h-6 w-6 text-gray-500" />
        </Button>
      ) : (
        <Button
          className="absolute bg-transparent top-6 right-1"
          size="sm"
          type="submit"
          variant="ghost"
          onClick={() => setIsListening(!isListening)}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M2.72403 2.05294C2.63791 2.0098 2.54115 1.99246 2.4454 2.003C2.34965 2.01355 2.25899 2.05152 2.18431 2.11236C2.10963 2.17321 2.05412 2.25432 2.02444 2.34597C1.99476 2.43761 1.99219 2.53587 2.01703 2.62894L3.51503 8.24694C3.53978 8.33958 3.59065 8.42315 3.66157 8.48769C3.73249 8.55223 3.82048 8.59501 3.91503 8.61094L10.77 9.75294C11.049 9.79994 11.049 10.1999 10.77 10.2469L3.91603 11.3889C3.82129 11.4047 3.7331 11.4474 3.66198 11.5119C3.59087 11.5765 3.53986 11.6602 3.51503 11.7529L2.01703 17.3709C1.99219 17.464 1.99476 17.5623 2.02444 17.6539C2.05412 17.7456 2.10963 17.8267 2.18431 17.8875C2.25899 17.9484 2.34965 17.9863 2.4454 17.9969C2.54115 18.0074 2.63791 17.9901 2.72403 17.9469L17.724 10.4469C17.807 10.4054 17.8767 10.3415 17.9255 10.2626C17.9742 10.1837 18 10.0927 18 9.99994C18 9.90716 17.9742 9.81622 17.9255 9.73728C17.8767 9.65833 17.807 9.59451 17.724 9.55294L2.72403 2.05294Z"
              fill="grey"
            />
          </svg>
        </Button>
      )}
    </div>
  );
}
