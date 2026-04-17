@echo off
title Servidor RosaIntelligence - MODULO DIRETO
echo ========================================================
echo   LIMPANDO PROCESSOS ANTIGOS...
taskkill /F /IM python.exe /T >nul 2>&1
echo   INICIANDO O MOTOR PYTHON E O AMBIENTE VIRTUAL...
echo ========================================================
echo.
echo ACESSE NO SEU NAVEGADOR: http://localhost:8501
echo.
echo Se o navegador nao abrir sozinho, copie o link acima.
echo.

:: Vai para a pasta exata do seu projeto
cd /d "C:\Users\ediney.junior\OneDrive\Engenheiro-Cientista-Analista de dados\Agente-IA"

:: Ativa o ambiente virtual correto
call venv\Scripts\activate

:: Inicia o Streamlit
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0

echo.
echo SE DEU ERRO ACIMA, CHAME O SUPORTE.
pause