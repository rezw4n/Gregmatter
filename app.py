import streamlit as st
import requests
from word_list.gregmat_list import group
from word_list.bangla import bangla_meaning
from word_list.data import meanings


st.set_page_config(
    page_title="Gregmatter",
    page_icon="📕",
    layout="centered",
    initial_sidebar_state="auto",
)

my_style = """<style>footer {visibility: hidden;}</style>"""

st.markdown(my_style, unsafe_allow_html=True)
st.title("Welcome to Gregmatter!")


def get_meaning(word):
    response = meanings.get(word)
    meaning = response[0]["meanings"]
    return meaning


@st.cache
def get_more_examples(word):
    examples = requests.get(
        f"https://corpus.vocabulary.com/api/1.0/examples/random.json?maxResults=64&query={word}&startOffset=0"
    ).json()
    return examples["result"]["sentences"]


study = (
    st.selectbox(
        "Select a group to study",
        options=[group_list.capitalize().replace("_", " ") for group_list in group],
    )
    .lower()
    .replace(" ", "_")
)

next_word = st.slider("Next and Previous word", min_value=0, max_value=29)

word = group.get(study)[next_word]

st.header(word.title())
st.write(bangla_meaning.get(word))

meaning = get_meaning(word)
for i in meaning:
    st.subheader(i["partOfSpeech"].title())
    for definition in i["definitions"]:
        st.markdown(f"**Definition:** {definition['definition'].capitalize()}")
        if len(definition["synonyms"]):
            st.markdown(f"**Synonyms:** {', '.join(definition['synonyms']).title()}")
        st.markdown(f"**Example:** {str(definition.get('example')).capitalize()}")


corpus = st.expander(label="More Examples from NYT or other sources:")

with corpus:
    index = 0
    more_example = get_more_examples(word)
    for example in more_example:
        if index == 10:
            st.markdown("\n")
            break
        if example["volume"]["corpus"]["name"] == "New York Times":
            index += 1
            st.markdown(f'{index}. {example["sentence"]}'.replace(word, f"**{word}**"))
    if index < 10:
        for example in more_example:
            if index == 10:
                st.markdown("\n")
                break
            index += 1
            st.markdown(f'{index}. {example["sentence"]}'.replace(word, f"**{word}**"))
