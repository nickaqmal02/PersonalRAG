"""testing wether our settings loading perfectly or not"""

from PersonalRAG.settings import settings

def main():
    print("=" * 50)
    print(" CURRENT SETTINGS ")
    print("=" * 50)

    # LLM
    print("\n LLM")
    print(f" API KEY {'set' if settings.groq_api_key else 'X Not Set'}")
    print(f" MODELL {settings.default_model}")
    print(f" TEMPERATURE: {settings.temperature}")
    print(f" MAX TOKENS: {settings.max_tokens}")

    #RAG
    print(f" RAG ")
    print(f" Chunk Size: {settings.chunk_size}")
    print(f" Chunk Overlap: {settings.chunk_overlap}")
    print(f" Top_K: {settings.top_k}")
    print(f" Score Threshold: {settings.score_threshold}")

    # PATHS
    print("\n Data Dir: {settings.data_dir}")

if __name__ == '__main__':
    main()

    
