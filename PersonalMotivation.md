# HEY NICKY LETS FINISH THIS PROJECT AND HIT THE BEST VERSION OF YOURSELF
- IF YOU WANNA DO IT ? DO IT !
- DO IT LIKE THIS IS YOUR LAST TIME GIVE THE BEST EFFORT AS YOU CAN

## THE 80/20 RULES OF LEARNING TO CODE

80% LEARNING HAPPENS BY BUILDING
20% LEARNING HAPPENS BY READING/WATCHING

# ALWAYS REMEMBER - EVERY ENGINEER STARTED HERE -

Year 1: "I don't know anything"
Year 2: "I know some things but I'm slow"
Year 3: "I know things but I make mistakes"
Year 5: "I know a lot but I learn constantly"
Year 10: "I know I don't know everything, and that's okay"

# THE BIGGEST DIFFERENCE BETWEEN JUNIOR AND SENIOR ENGINEERS IS ?
- JUNIORS: HIDE THEIR VULNERABILITIES
WHILE
- SENIORS: ACKNOWLEDGE AND ADDRESS THEIR VULNERABILITIES

## ====== PROJECT LEARNING DOCUMENTATION ======
BY @nick

- what is pyproject.toml 

- the differences between requirements.txt and pyproject.toml ??

- think like pyproject.toml -> the complete blueprint and build manual for your entire project.

- but requirements.txt like grocery list

- how to install all item in pyproject.toml

```
pip install -e .

```


## what does .strip() does ??
: let say
word = "$$AI$$"
print(word.strip("$")) -> AI 

## how do we find the page number and extract it


```python
\d any digit
\s any whitespace like space tab newline 
. any character 
* zero or more times
+ one or more times

(?i) dont care about the case sensitivity mate 
(?: group these options together but dont save them
page : page
p\.? p then maybe a dot
\s* any amount of space 
\d+ one or more digits


"""
the question is when do we shall use ? + at the end ??

+ when it shall have at least 1

? why this "?" 

for example we have

\s*[:.]?

? here means that, it could be no dot or even no double dot

without ? must exactly have one of it ? this is very crucial situation when building flexible big scales operation

is it every regex compulsory for us to put $ at the end r ' $'

ok so here is the explanation, I hope u gonna be thank you for yourself nicky in future

so here is the things


"""

let say 

r'\d+'

"Hello 42, then 99, and finally 100"

by not using $ at the end so what we can have is all the numbers 

so what we can do is 

ok before that when to use

re.search vs re.findall ??

use re.search() while u wanting the exact one value from that

use re.findall() while finding multiple input from the text 

'', text if we wanna just few words but 
'', document when multiple



    

```

## WHY WE NEED TO BUILD PERSONAL PROJECT ??
### WHY AND WHY AND WHY ??

- The story like this, 

A lot of successfull developer building their personal open-source project

example:

| DEVELOPER | WHAT THEY BUILT | WHY ? |
| --------------- | --------------- | --------------- |
| LINUS TORVALDS | LINUX | I WANTED FREE OS, SO I BUILT ONE  |


### lesson start

*what is sys ?: sys means for system *


## THE STRUCTURE OF OUR PROJECTNAME/CLI/MAIN.PY 

*How to really learn from this project* ??

#### all things that we really need to plan in our head 

```

What does user actually want ? 

### DEFINE USER GOALS

-> Load document ( which is ingestion )
-> Ask questions (chat)
-> Check system (status) by logger
-> See the version ()
-> Use TUI (tui)

~ the things is we shall start with user needs, not code 

### DEFINE COMMANDS

~ noted that, each user goal one CLI command

-> we use decorator from click documentation

@cli.command()
def ingest()...

### STEP 3: DEFINE WHAT INPUTS REALLY NEEDED

?? What does each command need ??

: so each command like 

- ingest: path, chunk_size, chunk_overlap
- chat: query, interactive, top_k





```


### Now what we need to do is check each method that needed for main application is working really well

> 
adding checking the method that needed for building and ensuring our main application working really well

##### METHOD IN OUR MAIN.PY needed for our main.py

- pipeline/rag_pipeline : RAGPipeline
- core/retriever : RAGRetriever
- core/vector_store : VectorStore
- llm/groq_provider : GroqProvider
- config/settings : settings
- 
settings.default_model ??
- 

> The question is, what does each function does ??
- settings.is_llm_configured 
- 

*what does the top_k means ??* it means that ??
top relevant document for our query





## DEVOPS ENGINEER / SYSTEM ENGINEER

> 10 BASIC COMMAND THAT WE ALWAYS NEED TO BE USE

- ls -l --color -la 
*
- passwd
- cat > cd.txt : to write and create new txt file
- cat ab.txt cd.txt > newfile : to connect both file together
- mv ab.txt abRename.txt
- ls -a : see hidden file
- ls -ltr : much more detail
- rm -rf abRename.txt
- cp abRename.txt path
- ps -f : displaying all current process that running right now
- k command to kill the process
- k -9 to kill the pid
- chmod to allow everyone to CRUD the file


## the differences between pass and continue

```python
for n in range(5):
    if n == 2:
        pass
    print(n)

# this will print 2 like normal but apart from that 

for i in range(5):
    if i == 2:
        continue
    print(n)

# not printing the 2 value actually

# another one ins break directly
for n in range(5):
    if n == 2:
        break
    print(n)

# this will break directly from that loop
```
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
### GIT LESSON
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::

```

# removing the .env if staged which is still not push and not commit yet
git rm --cached .env

# removing the .env if commited but not push yet
git rm --cached .env
git commit --amend

# if env was commited and push
git filter-repo --path .env --invert-paths --force

git remote add origin <url>

git push origin --force --all

# Conventional commits style:

feat: new feature
fix: bug fix 
test: tests
docs: documentation
chore: maintenance


```
#### ::::::::::::::::::::::::
#### ::::::::::::::::::::::::
#### ::::::::::::::::::::::::
### NVIM PROFICIENCY
#### ::::::::::::::::::::::::
#### ::::::::::::::::::::::::
#### ::::::::::::::::::::::::

**DELETING EVERYTHING**
```
di: delete inside
ci: deletes inside and be into insert mode

da: delete around the quotes
ca: delete around the quotes and be into insert mode

so ?? 
q means quote
b for a whole []
B only latest {}

how to apply then ??

the snippets 

diq : means delete inside quotes
ciq : means delete inside quotes and be into insert mode

daq : means delete around quotes
caq : means delete around quotes and be into insert mode

```
~ nick, 18 sept 26

**JUMPING INTO BLOCK AND DOUBLE QUOTES**

```
t"la : go into this quotes and be in insert mode

esc to be in normal mode 

caps lock and shift + i to be in first start syntax of the line

```

#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
### AEROSPACE TILING MANAGEMENT
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::

```
alt-comma: accordion
alt-slash: horizontal

alt-z: fullscreen
alt-x: close window

alt-shift-l: means we focus on current focus windows to left means prioritize it more
alt-shift-r: means we focus current focus into right

then how to change focus to another windows

```



#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::
### SOFTWARE ENGINEERING LESSON 
#### ::::::::::::::::::::::::::
#### ::::::::::::::::::::::::::



```

# in clean design we use wrapper to wrap all method for that particular field

lets say we have Embedding function 

class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def ...

    def ...


    def get_dimenstion(self) -> int:
        return self.model.get_sentence_embedding_dimension()

#  alot of lesson from this journey 
- type annotation
- wrapper
- why use type annotation, because we can use mypy to check the error


```

##### HOW WE FIX THE CORE PROBLEM DISTANCE AND SIMILARITY AND HOW DOES THE VECTOR DB PASS THE DISTANCE...  [19/09/26] 0020H

```

CHROMADB RETURNS "DISTANCE"

SO WE USE COSINE SIMILARITY SCALE

-1 - 0 - +1

THE FORMULA:

(2 - DISTANCE) / 2

because what chromadb give to us, is not accurate and what we want so

Distance Ruler (ChromaDB gives this):
0 ─────────────── 1 ─────────────── 2
"Identical"     "Different"      "Opposite"

Similarity Ruler (What we want):
0 ─────────────── 0.5 ─────────────── 1
"No match"      "Some match"       "Perfect match"

They're OPPOSITE directions!

is it any problem with it ??

ok let say if distance = 0.5 its ok 

to use 1 - distance but if 1.5 it becames -0.5 wrong

so we flip the meaning

using (2 - d) / 2

so if distance is 2 from vector db we use **cosine** as a space declaration

statig to our metadata collection 

"hnsw:space": "cosine" which is [0, 2]

cosine good for text embeddings 

hnsw the algorithm
cosine ditance metrix 
:
hnsw = The search engine ( how to find neighbors )
space = the ruler how we measure the distance

```

## ABOUT RAG

> RAG have several Design Patterns 
- Naive RAG 
- retrieve and rerank
- multimodal RAG
- Graph RAG
- Hybrid RAG
- Agentic RAG
- Agent RAG 

~ so my application use which one ?



#### :::::::::::::::::::::::::::::::::::
#### :::::::::::::::::::::::::::::::::::
#### :::::::::::::::::::::::::::::::::::
### WHY I SHALL BUILD THIS SOFTWARE
#### :::::::::::::::::::::::::::::::::::
#### :::::::::::::::::::::::::::::::::::
#### :::::::::::::::::::::::::::::::::::

1. It's proof that you can build real software
2. It combines AI + Engineering
3. It's portfolio piece that demos itself
4. It's foundation for everything

> **PersonalRAG isn't just a project. It's your ticker**




### TEXTUAL TUI FRAMEWORKS

> What methods we provide. Textual decides when to call them

```

What provide

- __init__() -> When created do this
- compose() -> Build the UI like this
- on_mount() ->  When ready ok do this
- on_input_submitte() -> when enter pressed, do this 
- action_clear() -> when Ctrl+L pressed, do this





```

What is **RichLog**


Why by using simple direct command syntax we can use the engine of RAGPipeline ??

because the TUI version, are event driven application

```

Textual framework runs:
  ↓
Event loop is ALWAYS running
  ↓
You press Enter → event fires → handler runs
  ↓
Handler must return QUICKLY
  ↓
Textual keeps looping (waiting for next event)

so we use asyncio.to_thread to run the blocking RAG pipeline in the background, then call_from_thread to update the UI safely.

```

so mostly we do synchronous programming
which means we can do some task while waiting another task to finish


# THIS IS THE REAL TRADE OFF BETWEEN USING ASYNC VS THREADING
> I actually built a RAG Agent with a textual TUI. The RAG pipeline uses Sentence Transformers, which CPU-heavy and blocking

> I first tried asyncio.to_thread(), but it crashed on macOS

> What is different between thread and process

**Process**:= A running program with its own memory
**Thread**:= A worker inside a process, sharing memory

**The Key takeaway: One process can have many threads. One thread belongs to one process**


```
┌─────────────────────────────────────────┐
│           PROCESS                       │
│  (Own memory, own file descriptors)     │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Thread 1 │  │ Thread 2 │  │Thread 3│ │
│  │ (main)   │  │ (worker) │  │(worker)│ │
│  └──────────┘  └──────────┘  └────────┘ │
│                                         │
│  All threads share the same memory      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│           PROCESS 2                     │
│  (Separate memory)                      │
│                                         │
│  ┌──────────┐  ┌──────────┐             │
│  │ Thread 1 │  │ Thread 2 │             │
│  └──────────┘  └──────────┘             │
└─────────────────────────────────────────┘

```
**Processes are isolated. But threads are share.**

**what does it mean run_worker**

```
use-case example

self.run_worker(self.process_query(query))


```

"My RAG agent uses the Naive RAG pattern - retrieve, build context, generate. Im planning to add reranking next using a cross-encoder, which typically improves retrieval quality by 20-30%. After that I will explore hybrid search combining vector and BM25, and eventually agentic RAG where the agent decides when to retrieve"


