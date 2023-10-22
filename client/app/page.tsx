"use client";
import { cn } from "@/lib/utils";
import * as React from "react";
// import { useChat } from "ai/react";
import { ArrowDown, User2Icon } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useToast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import SpeechInput from "@/components/speech-input";

export default function Home() {
  const formRef = React.useRef<HTMLFormElement>(null);
  const { toast } = useToast();
  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const [language, setLanguage] = React.useState("en");
  const [prompt, setPrompt] = React.useState("");

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // formRef.current?.reset();
    // setIsDialogOpen(true);
  };

  // Scroll to the last message whenever messages updates
  // React.useEffect(() => {
  //   if (messagesEndRef.current) {
  //     scrollToBottom();
  //   }
  // }, [messages]);

  // const disabled = isLoading || input.length === 0;

  React.useEffect(() => {
    console.log(language);
  }, [language]);

  return (
    <>
      <header className="container flex justify-between items-center h-14">
        <div className="flex gap-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            className="lucide lucide-book-a"
          >
            <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
            <path d="m8 13 4-7 4 7" />
            <path d="M9.1 11h5.7" />
          </svg>
          <span className="font-bold text-primary">NYCGIA</span>
        </div>
        <Select
          onValueChange={(value) => {
            setLanguage(value);
          }}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="English" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="en-US">English</SelectItem>
            <SelectItem value="es-ES">Spanish</SelectItem>
            <SelectItem value="hi-INB">Hindi</SelectItem>
          </SelectContent>
        </Select>
      </header>
      <main className="w-full container relative display flex flex-col flex-grow overflow-y-auto mx-auto flex-1 pb-60 md:pb-44">
        <section className="w-full mt-4 mx-auto max-w-3xl ">
          {/* <ul className="w-full flex flex-col gap-8 px-4">
            {messages.map((m, index) => (
              <li key={index} className="w-full flex gap-4">
                <div className="text-primary">
                  {m.role === "user" ? (
                    <div className="border border-primary/[8%] inline-flex items-center rounded-full p-2 sm:p-[8px] bg-primary/[8%]">
                      <User2Icon className="w-6 h-6 p-0.5" />
                    </div>
                  ) : (
                    <div className="bg-primary inline-flex items-center rounded-full p-2">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-6 sm:h-[25px] w-6 sm:w-[25px]"
                        viewBox="0 0 29 30"
                        fill="none"
                      >
                        <path
                          d="M9.01904 20.3403L10.1651 23.8656C10.1978 23.9661 10.2562 24.0563 10.3346 24.1271C10.413 24.198 10.5086 24.2471 10.6118 24.2694C10.7151 24.2918 10.8224 24.2867 10.9231 24.2547C11.0238 24.2226 11.1143 24.1647 11.1856 24.0867L16.2956 18.5127"
                          stroke="black"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="1.33"
                        />
                        <path
                          d="M22.8895 15.6269C22.8895 15.6269 22.2491 19.0205 18.4616 19.0205C14.674 19.0205 12.287 14.3467 9.4341 14.3467C6.06406 14.3467 5.17896 17.176 5.17896 19.0205C5.17896 20.595 6.01512 21.2348 7.12196 21.2348C8.22879 21.2348 10.295 19.3649 11.1807 18.4055H16.0745"
                          stroke="black"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="1.33"
                        />
                        <path
                          d="M9.43406 14.347C9.43406 12.7236 8.13027 11.4688 6.08879 11.4688C4.04731 11.4688 2.71875 12.4777 2.71875 15.3306C2.71875 18.1835 5.18556 18.749 5.18556 18.749"
                          stroke="black"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="1.33"
                        />
                        <path
                          d="M4.38375 11.7989C3.61404 9.76771 5.52261 7.7794 8.47457 7.7794C12.9514 7.7794 13.3568 15.0475 17.6494 15.0475C21.2164 15.0475 23.6083 10.4214 21.9789 7.75523C19.8142 4.2124 16.1946 4.86369 14.6691 6.31489"
                          stroke="black"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="1.33"
                        />
                        <path
                          d="M8.47461 7.77907C9.28661 5.04824 13.3575 4.96244 14.9688 6.57376C16.5801 8.18507 16.4937 10.4845 14.2329 13.0033M19.9634 14.347C21.6962 16.4495 25.9556 16.157 26.2631 11.9877C26.5706 7.81834 22.9202 7.8854 22.191 8.16453"
                          stroke="black"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="1.33"
                        />
                      </svg>
                    </div>
                  )}
                </div>
                <ReactMarkdown
                  className={`prose w-full break-words prose-p:leading-relaxed sm:pt-2 ${
                    m.role === "user" ? "text-primary" : "text-primary/70"
                  }`}
                  remarkPlugins={[remarkGfm]}
                  components={{
                    a: (props) => (
                      <a
                        {...props}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary/70"
                      />
                    ),
                  }}
                >
                  {m.content}
                </ReactMarkdown>
              </li>
            ))}
            <div ref={messagesEndRef} />
          </ul> */}
        </section>
      </main>
      <footer className="fixed bottom-0 w-full flex flex-col items-center space-y-2 p-5 pb-3 sm:px-0">
        {/* <div className="w-full flex justify-end sm:pr-6">
          {messages.length > 0 && (
            <Button
              size="sm"
              className="mt-2 sm:fixed r-4 rounded-full py-1 px-2.5 bg-neutral-800 hover:bg-neutral-700 text-primary border border-primary/[8%] hover:bg-primary/[8%] hover:border-white/25 hover:text-primary"
              variant="ghost"
              onClick={scrollToBottom}
            >
              <ArrowDown className="w-4 h-4 text-primary" />
            </Button>
          )}
        </div> */}
        <div className="w-full max-w-3xl mx-auto">
          <div className="mx-auto flex w-full max-w-[750px] md:px-6 lg:px-0">
            <div className="flex-grow"></div>
            dialo
          </div>
          <form
            className="w-full max-w-[750px] md:px-6 lg:px-0 relative py-[10px] mx-auto "
            onSubmit={handleSubmit}
          >
            {/* <Textarea
              className={cn(
                "h-[50px] relative w-full max-w-screen-md  border border-gray-200 bg-white px-4 pb-2  shadow-lg sm:pb-3 sm:pt-4 items-center max-h-[200px] max pt-3 resize-none rounded-xl"
              )}
              placeholder="Type your message here."
              value={prompt}
              autoFocus
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  formRef.current?.requestSubmit();
                  e.preventDefault();
                }
              }}
            />
            <Button
              className="absolute bg-transparent top-6 right-1 hover:bg-transparent"
              size="sm"
              type="submit"
              variant="ghost"
              // disabled={disabled}
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
            </Button> */}
            <SpeechInput language={language} />
          </form>
          <div className="pb-3 text-center text-xs px-2 md:px-[60px]">
            <p className="text-center text-xs text-primary/60">
              This project waas built with{" "}
              <a
                href="https://platform.openai.com/docs/guides/gpt/function-calling"
                target="_blank"
                rel="noopener noreferrer"
                className="transition-colors hover:text-primary-foreground"
              >
                OpenAI Functions
              </a>{" "}
              and{" "}
              <a
                href="https://sdk.vercel.ai/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="transition-colors hover:text-primary-foreground"
              >
                Vercel AI SDK
              </a>
              .{" "}
              <a
                href="https://github.com/JaleelB/ask-yelp"
                target="_blank"
                rel="noopener noreferrer"
                className="transition-colors hover:text-primary-foreground"
              >
                View the project repo here.
              </a>
            </p>
          </div>
        </div>
      </footer>
    </>
  );
}
