@echo off
echo ==============================================
echo Instalador de Dependencias de Inventario
echo ==============================================
echo Verificando instalacion de Python e instalando requerimientos...
echo.

python -m pip install --upgrade pip
pip install -r requirements.txt

echo.