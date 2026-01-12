from google.adk.agents import SequentialAgent
from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.apps import App
from google.adk.apps.app import EventsCompactionConfig


MODEL = 'gemini-2.5-flash'

classifyng_agent = LlmAgent(
    name='ClassifyngAgent',
    model=MODEL,
    instruction="""
        Você é um classificador de sentimentos em analises de produtos de E-Commerce
        Baseado *apenas* no comentario fornecido pelo usuário, classifique a analise entre os sentimentos:
        
        - POSITIVO
        - NEUTRO
        - NEGATIVO
        
        Saida deve ser apenas o sentimento analizado juntamente ao texto da review no formato de json seguindo o seguinte exemplo:
        
        {"analise": "texto_da_analise: str", "sentimento": "sentimento: str"}
        
        Não adicione quaisquer informações adicionais, explicações ou  introduções
    """,
    description="Agente resposável por classificar o sentimento do usuário",
    output_key="classificação_sentimento"
)

report_agent = LlmAgent(
    name='ReportAgent',
    model=MODEL,
    instruction="""
        Você é resposável por identificar o problema que esta sendo relatado pelo usuario
        baseado no sentimento e na analise {classificação_sentimento}, 
        
        ## Caso o sentimento seja NEGATIVO, identifique quais as caracristicas que causasaram a analise negativa e sugira pontos de melhora.
        ## Caso o sentimento seja POSITIVO ou NEUTRO, identifique quais as caracteristicas que agradaram o usuário
        
        A saida deve ser um JSON seguindo a sequinte estrutura:
        
        {
            "analise": "texto_da_analise: str", 
            "sentimento": "sentimento: str",
            "caracristicas_negativas": str,
            "caracristicas_positivas": str,
            "pontos_melhora": str
        }
        
        Não adicione quaisquer informações adicionais, explicações ou  introduções
    """
)

resolver_agent = LlmAgent(
    name='ResolverAgent',
    model=MODEL,
    instruction="""
        Você é responsável por responder os comentarios do usuário de maneira empatica, baseando se na analise de sentimento
        presente em {classificação_sentimento}
        
        Responda de maneira cordial e simpática, em caso de analise NEGATIVA indique que a equipe de atendimento ao cliente
        irá entrar em contato para resolver o problema
        
        A saida deve ser um JSON seguindo a sequinte estrutura:
        {
            "analise": "texto_da_analise: str", 
            "sentimento": "sentimento: str",
            "resposta_empatica": str
        }
    """,
    description="Agente responsavel por formatar uma resposta empatica para o cliente"
)

sentiment_analyzer = SequentialAgent(
    name='SentimentAnalyzer',
    sub_agents=[classifyng_agent, report_agent, resolver_agent],
    description="Analise de sentimento de reviews de comentarios em ECommerce",
)

root_agent = Agent(
    name='RootAgent',
    model=MODEL,
    sub_agents=[sentiment_analyzer],
    instruction="""
        Repasse apenas o JSON final gerado pelo sub-agente, sem comentários.
    """
)
