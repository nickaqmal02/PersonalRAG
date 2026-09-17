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


