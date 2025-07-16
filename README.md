JOGO DE ADIVINHAÇÃO DE PALAVRAS - DESAFIO DE RIVAIS
====================================================

**Autor:** JailtonGN
**Versão:** 1.0

---

# OBJETIVO
Descubra a palavra secreta sorteada (modo solo) ou definida por outro jogador (modo multiplayer), letra por letra, no menor tempo possível e com o menor número de erros!

---

# MODOS DE JOGO

- **Solo:**
  - O sistema sorteia uma palavra aleatória do dicionário, conforme a dificuldade escolhida.
  - Você deve adivinhar a palavra, letra por letra, usando as letras embaralhadas como dica.
  - Seu tempo e número de erros contam para o ranking.

- **Multiplayer:**
  - Os jogadores se revezam: um define a palavra, o outro tenta adivinhar.
  - Cada palavra deve ter entre 4 e 20 letras.
  - Ao final, o ranking mostra o desempenho de cada jogador e as palavras mais usadas.

---

# REGRAS DE DIFICULDADE (MODO SOLO)
- **Fácil:** Palavras de 4 ou 5 letras
- **Médio:** Palavras de 6 ou 7 letras
- **Difícil:** Palavras de 8 a 20 letras

No multiplayer, a dificuldade não limita o tamanho da palavra (apenas 4 a 20 letras).

---

# FUNCIONALIDADES
- Dicionário customizável (pt_BR.dic ou palavras.txt)
- Sugestão de palavras e correção ortográfica
- Ranking solo (Top 10 por dificuldade)
- Ranking multiplayer (palavras mais usadas)
- Definição online (Wiktionary)
- Sons e música customizáveis
- Tema visual confortável (amarelo pastel)
- Persistência de palavras já sorteadas (evita repetição)
- Suporte a modo tela cheia

---

# INSTALAÇÃO E EXECUÇÃO

1. **Pré-requisitos:**
   - Python 3.8 ou superior
   - Instale as dependências:
     - tkinter (normalmente já incluso)
     - pygame
     - requests
     - beautifulsoup4

   Exemplo de instalação:
   ```sh
   pip install pygame requests beautifulsoup4
   ```

2. **Execute o jogo:**
   ```sh
   python Jogo.py
   ```

3. **Arquivos importantes:**
   - `Jogo.py` — código principal
   - `palavras.txt` ou `pt_BR.dic` — dicionário de palavras
   - `sons/` — pasta com arquivos de som
   - `ranking_solo.json`, `palavras_usadas.json` — arquivos de dados gerados automaticamente

---

# DICAS
- Use as letras embaralhadas para ajudar na adivinhação.
- Errar uma letra adiciona penalidade de tempo.
- No multiplayer, escolha palavras que os outros jogadores conheçam!
- O botão "Ver definição" abre a página do Wiktionary para a palavra.
- O jogo salva seu progresso e ranking automaticamente.

---

# CONTATO E CONTRIBUIÇÃO
- Para dúvidas, sugestões ou bugs, entre em contato com o autor.
- Sinta-se livre para modificar e melhorar o jogo!

---

Divirta-se e desafie seus amigos!
