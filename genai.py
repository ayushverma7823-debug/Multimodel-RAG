import google.generativeai as genai
genai.configure(api_key="AQ.Ab8RN6IVvKBFRGlT2zJyTVmHLqAu5Z0AfdTLWW2IXSBcSxiMDw")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)