# classifier.py
# Contém funções para extrair texto, pré-processar, classificar e gerar resposta com Gemini.
import os
import re
from typing import Dict
import google.generativeai as genai
from PyPDF2 import PdfReader

# Carrega a chave de API do Gemini do ambiente
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    GEMINI_AVAILABLE = True
except Exception as e:
    print(f"Erro ao configurar Gemini: {e}")
    GEMINI_AVAILABLE = False

# Simple stopwords (pt-BR small set)
STOPWORDS = set("""a o e de do da em no na os as dos das um uma uns umas com por para como sobre que quem quando onde porque pelo""".split())

def extract_text_from_file(file_stream, filename: str) -> str:
    """Extrai texto de um arquivo .pdf ou .txt a partir de um stream."""
    filename = filename.lower()
    if filename.endswith('.pdf'):
        try:
            reader = PdfReader(file_stream)
            texts = [p.extract_text() or '' for p in reader.pages]
            return '\n'.join(texts)
        except Exception:
            return ''
    elif filename.endswith('.txt'):
        try:
            return file_stream.read().decode('utf-8', errors='ignore')
        except Exception:
            return ''
    return ''

def simple_preprocess(text: str) -> str:
    """Limpeza básica do texto."""
    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'[^\w\sÀ-ÿ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = [t for t in text.split() if t not in STOPWORDS]
    return ' '.join(tokens)

def gemini_classify_and_respond(text: str) -> Dict[str, str]:
    """Usa a API do Gemini para classificar e gerar uma resposta."""
    if not GEMINI_AVAILABLE:
        raise RuntimeError('API Key do Gemini não configurada.')

    model = genai.GenerativeModel('gemini-pro')

    # Prompt para classificação
    prompt_classify = f"""
    Classifique o seguinte email como 'Produtivo' ou 'Improdutivo'.
    'Produtivo' se o email exigir uma ação ou resposta específica (suporte, dúvida, status).
    'Improdutivo' se for um email genérico (agradecimento, felicitação).
    Retorne apenas uma única palavra: Produtivo ou Improdutivo.

    Email: "{text[:3000]}"
    """
    response_classify = model.generate_content(prompt_classify)
    category = response_classify.text.strip()

    # Define o prompt de resposta com base na categoria
    if 'produtivo' in category.lower():
        prompt_reply = f"""
        Você é um assistente de email corporativo.
        Com base no email abaixo, gere uma resposta curta, educada e profissional em português.
        Se necessário, peça mais informações para dar continuidade ao atendimento.

        Email original: "{text[:2000]}"
        """
    else:
        prompt_reply = f"""
        Você é um assistente de email corporativo.
        O email abaixo foi classificado como improdutivo (agradecimento ou felicitação).
        Gere uma resposta de cortesia curta e educada em português.

        Email original: "{text[:2000]}"
        """

    response_reply = model.generate_content(prompt_reply)
    reply = response_reply.text.strip()

    return {'category': category, 'response': reply}


def classify_and_respond(text: str, use_gemini: bool = True) -> Dict[str, str]:
    """Função principal que orquestra a classificação e resposta."""
    if not text or not text.strip():
        return {'category': 'Improdutivo', 'response': 'Não foi possível extrair conteúdo do email.'}

    if use_gemini and GEMINI_AVAILABLE:
        try:
            return gemini_classify_and_respond(text)
        except Exception as e:
            print(f"Erro na API do Gemini, usando fallback: {e}")
            # Se a API falhar, usa o método baseado em regras
            return rule_based_classify_and_respond(text)
    else:
        # Se Gemini não estiver disponível, usa o método baseado em regras
        return rule_based_classify_and_respond(text)


def rule_based_classify_and_respond(text: str) -> Dict[str, str]:
    """Classificador simples baseado em palavras-chave como alternativa."""
    pp_text = simple_preprocess(text)
    
    PRODUCTIVE_KEYWORDS = ['erro','problema','suporte','ajuda','ticket','status','atualiza','documento','anexo','preciso','urgente','falha','corrigir','retorno', 'solicito']
    IMPRODUCTIVE_KEYWORDS = ['feliz','parabéns','obrigado','obrigada','bom trabalho', 'agradeço']

    prod_score = sum(1 for k in PRODUCTIVE_KEYWORDS if k in pp_text)
    imp_score = sum(1 for k in IMPRODUCTIVE_KEYWORDS if k in pp_text)

    if prod_score > imp_score:
        category = 'Produtivo'
        reply = 'Obrigado pelo contato. Recebemos sua solicitação e retornaremos em breve. Para agilizar, poderia nos fornecer o número do protocolo ou mais detalhes sobre o caso?'
    else:
        category = 'Improdutivo'
        reply = 'Obrigado pela sua mensagem!'
        
    return {'category': category, 'response': reply}