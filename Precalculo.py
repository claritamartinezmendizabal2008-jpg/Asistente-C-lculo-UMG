# -- coding: utf-8 --
"""
AulaCálculo - Asistente virtual académico de precálculo y cálculo
Instalación:
    pip install streamlit sympy numpy matplotlib
Ejecución:
    streamlit run asistente_calculo.py

Personaliza INTEGRANTE_1, INTEGRANTE_2, ASIGNATURA y SECCION antes de entregar.
"""

import random
import math
import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# ==================== DATOS DEL PROYECTO ====================
NOMBRE_ASISTENTE = "AulaCálculo"
INTEGRANTE_1 = "Greisy Paola Temaj Miranda"
INTEGRANTE_2 = "Sulma Clarita Martinez Mendizabal"
ASIGNATURA = "Precalculo"
SECCION = "B"

x, y = sp.symbols("x y", real=True)

st.set_page_config(page_title=NOMBRE_ASISTENTE, page_icon="📘", layout="wide")

# ==================== FUNCIONES DE CÁLCULO ====================
def parse_expr(texto):
    """Convierte texto matemático a una expresión de SymPy de forma controlada."""
    texto = texto.strip().replace("^", "*").replace("÷", "/").replace("×", "")
    if not texto:
        raise ValueError("Escribe una expresión antes de continuar.")
    permitidos = {
        "x": x, "y": y, "pi": sp.pi, "e": sp.E,
        "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
        "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
        "sqrt": sp.sqrt, "log": sp.log, "ln": sp.log,
        "exp": sp.exp, "abs": sp.Abs
    }
    return sp.sympify(texto, locals=permitidos)

def mostrar_procedimiento(titulo, formula, pasos, resultado):
    st.subheader(titulo)
    st.markdown(f"*Fórmula o regla:* {formula}")
    for i, paso in enumerate(pasos, 1):
        st.write(f"{i}. {paso}")
    st.success(f"*Respuesta final:* {sp.simplify(resultado)}")

def resolver_ecuacion(ecuacion):
    expr = parse_expr(ecuacion)
    st.markdown("*Ecuación ingresada:*")
    st.latex(sp.latex(sp.Eq(expr, 0)))
    st.markdown("*Procedimiento:*")
    st.write("1. Se pasa todo al lado izquierdo para igualar la expresión a cero.")
    st.write("2. Se busca el valor de x que hace verdadera la igualdad.")
    resultado = sp.solve(sp.Eq(expr, 0), x)
    st.write("3. Se resuelve la ecuación con métodos algebraicos simbólicos.")
    st.success(f"*Solución(es):* {resultado if resultado else 'No se encontraron soluciones simbólicas.'}")
    return resultado

def graficar(expr, xmin, xmax):
    f = sp.lambdify(x, expr, modules=["numpy"])
    xs = np.linspace(xmin, xmax, 700)
    with np.errstate(all="ignore"):
        ys = f(xs)
    if np.isscalar(ys):
        ys = np.full_like(xs, float(ys))
    ys = np.asarray(ys, dtype=float)
    ys[~np.isfinite(ys)] = np.nan
    fig, ax = plt.subplots()
    ax.plot(xs, ys, label=f"f(x) = {sp.sstr(expr)}")
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.grid(True, alpha=0.35)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Gráfica de la función")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

# ==================== ENCABEZADO ====================
st.title("📘 AulaCálculo")
st.write("Asistente virtual académico para practicar álgebra, funciones y cálculo.")
st.caption(f"Integrantes: {INTEGRANTE_1} y {INTEGRANTE_2}  |  Asignatura: {ASIGNATURA}  |  Sección: {SECCION}")
st.info("Escribe potencias con ** o ^. Ejemplos: x^2+3*x+2, sin(x), sqrt(x). Usa * para multiplicar.")

with st.sidebar:
    st.header("Menú")
    modulo = st.radio("Selecciona un módulo:", [
        "Inicio y ejemplos", "Álgebra y funciones", "Representación gráfica",
        "Límites", "Derivadas", "Integrales", "Aplicaciones",
        "Práctica con retroalimentación"
    ])
    st.divider()
    st.caption("Este asistente ayuda a estudiar. Comprueba los resultados y consulta a tu docente cuando sea necesario.")

# ==================== INICIO Y EJEMPLOS ====================
if modulo == "Inicio y ejemplos":
    st.header("¡Bienvenido!")
    st.write("Selecciona un módulo en el menú para resolver ejercicios nuevos paso a paso.")
    st.subheader("10 ejercicios de ejemplo")
    ejemplos = [
        ("Ecuación lineal", "2*x - 8", "Solución: x = 4"),
        ("Ecuación cuadrática", "x^2 - 5*x + 6", "Soluciones: x = 2 y x = 3"),
        ("Factorización", "x^2 - 9", "(x - 3)(x + 3)"),
        ("Derivada", "x^3 - 6*x^2 + 9*x + 1", "3*x^2 - 12*x + 9"),
        ("Integral indefinida", "3*x^2 + 2*x", "x^3 + x^2 + C"),
        ("Límite", "(x^2 - 1)/(x - 1)", "Límite cuando x tiende a 1: 2"),
        ("Evaluación", "x^2 + 2*x + 1", "Para x = 2, resultado: 9"),
        ("Raíces", "x^2 + 4*x + 4", "Raíz: x = -2"),
        ("Punto crítico", "x^2 - 4*x + 1", "Punto crítico en x = 2"),
        ("Composición", "(x + 1)^2", "Ejemplo de función compuesta")
    ]
    for i, (nombre, expresion, resultado) in enumerate(ejemplos, 1):
        with st.expander(f"{i}. {nombre}"):
            st.code(expresion)
            st.write(resultado)
    st.caption("Los ejemplos son una guía inicial. Los módulos calculan expresiones que ingrese el usuario.")

# ==================== ÁLGEBRA ====================
elif modulo == "Álgebra y funciones":
    st.header("Álgebra y funciones")
    operacion = st.selectbox("Operación", [
        "Resolver ecuación (igualada a cero)", "Factorizar",
        "Expandir", "Simplificar", "Evaluar función",
        "Dominio (restricciones reales)", "Composición de funciones"
    ])
    if operacion == "Composición de funciones":
        ftxt = st.text_input("f(x) =", "x^2 + 1")
        gtxt = st.text_input("g(x) =", "2*x")
    else:
        texto = st.text_input("Expresión matemática", "x^2 - 5*x + 6")
    if operacion == "Evaluar función":
        valor = st.number_input("Valor de x", value=2.0)
    if st.button("Resolver", type="primary"):
        try:
            if operacion == "Resolver ecuación (igualada a cero)":
                resolver_ecuacion(texto)
            elif operacion == "Factorizar":
                expr = parse_expr(texto)
                mostrar_procedimiento("Factorización", "Expresar como producto de factores",
                    [f"Expresión original: {sp.sstr(expr)}", "Se identifican factores algebraicos."],
                    sp.factor(expr))
            elif operacion == "Expandir":
                expr = parse_expr(texto)
                mostrar_procedimiento("Expansión", "Aplicar la propiedad distributiva",
                    ["Se multiplican los términos y se agrupan términos semejantes."], sp.expand(expr))
            elif operacion == "Simplificar":
                expr = parse_expr(texto)
                mostrar_procedimiento("Simplificación", "Reducir la expresión a una forma equivalente",
                    ["Se aplican identidades y se combinan términos semejantes."], sp.simplify(expr))
            elif operacion == "Evaluar función":
                expr = parse_expr(texto)
                res = expr.subs(x, valor)
                mostrar_procedimiento("Evaluación", f"f({valor})", 
                    [f"Se sustituye cada x por {valor}.", f"Se calcula {sp.sstr(expr.subs(x, sp.Float(valor)))}."], res)
            elif operacion == "Dominio (restricciones reales)":
                expr = parse_expr(texto)
                st.write("*Expresión:*")
                st.latex(sp.latex(expr))
                st.write("Para hallar el dominio, identifica denominadores que no pueden ser cero y raíces pares cuyo interior debe ser no negativo. Para expresiones complicadas, revisa las restricciones indicadas por la expresión.")
                st.write("*Denominadores:*", sp.denom(sp.together(expr)))
                st.write("*Restricciones detectables:*", sp.solve(sp.Ne(sp.denom(sp.together(expr)), 0), x) if sp.denom(sp.together(expr)) != 1 else "No hay denominador.")
            else:
                fexpr, gexpr = parse_expr(ftxt), parse_expr(gtxt)
                resultado = sp.simplify(fexpr.subs(x, gexpr))
                mostrar_procedimiento("Composición f(g(x))", "f ∘ g = f(g(x))",
                    [f"f(x) = {sp.sstr(fexpr)}", f"g(x) = {sp.sstr(gexpr)}", "Se sustituye x en f por toda la expresión g(x)."],
                    resultado)
        except Exception as e:
            st.error(f"No se pudo resolver. Revisa los datos y la sintaxis. Detalle: {e}")

# ==================== GRÁFICAS ====================
elif modulo == "Representación gráfica":
    st.header("Representación gráfica")
    texto = st.text_input("Función f(x) =", "x^3 - 6*x^2 + 9*x + 1")
    col1, col2 = st.columns(2)
    xmin = col1.number_input("x mínimo", value=-5.0)
    xmax = col2.number_input("x máximo", value=5.0)
    if st.button("Graficar función", type="primary"):
        try:
            if xmin >= xmax:
                st.error("El valor mínimo de x debe ser menor que el máximo.")
            else:
                expr = parse_expr(texto)
                graficar(expr, xmin, xmax)
                st.write("*Intersecciones con el eje x (raíces):*", sp.solve(expr, x))
                st.write("*Intersección con el eje y:*", expr.subs(x, 0))
                st.write("La gráfica permite observar intervalos de crecimiento/decrecimiento y puntos importantes.")
        except Exception as e:
            st.error(f"No se pudo graficar. Verifica la función. Detalle: {e}")

# ==================== LÍMITES ====================
elif modulo == "Límites":
    st.header("Cálculo de límites")
    texto = st.text_input("Función", "(x^2 - 1)/(x - 1)")
    punto_txt = st.text_input("x tiende a", "1")
    direccion = st.selectbox("Dirección", ["Ambos lados", "Por la izquierda", "Por la derecha"])
    if st.button("Calcular límite", type="primary"):
        try:
            expr, punto = parse_expr(texto), parse_expr(punto_txt)
            dir_map = {"Ambos lados": "+-", "Por la izquierda": "-", "Por la derecha": "+"}
            res = sp.limit(expr, x, punto, dir=dir_map[direccion])
            st.markdown("*Procedimiento:*")
            st.write("1. Se identifica la función y el valor al que tiende x.")
            st.write("2. Se intenta la sustitución directa; si aparece una indeterminación, se simplifica o se aplica un método de límites.")
            st.write("3. Se evalúa el límite con el método simbólico.")
            st.latex(r"\lim_{x\to " + sp.latex(punto) + "} " + sp.latex(expr) + " = " + sp.latex(res))
            st.success(f"Respuesta final: {res}")
        except Exception as e:
            st.error(f"No se pudo calcular el límite. Revisa la entrada. Detalle: {e}")

# ==================== DERIVADAS ====================
elif modulo == "Derivadas":
    st.header("Derivadas")
    texto = st.text_input("Función f(x)", "x^3 - 6*x^2 + 9*x + 1")
    orden = st.selectbox("Orden de derivación", [1, 2, 3, 4])
    if st.button("Derivar", type="primary"):
        try:
            expr = parse_expr(texto)
            res = sp.diff(expr, x, orden)
            st.markdown("*Procedimiento:*")
            st.write("1. Se identifica la función.")
            st.write("2. Se aplican las reglas de derivación: potencia, suma, producto, cociente o cadena según corresponda.")
            st.write(f"3. Se deriva {orden} vez/veces y se simplifica el resultado.")
            st.latex(r"f^{(" + str(orden) + r")}(x) = " + sp.latex(res))
            st.success(f"Respuesta final: {res}")
            if orden == 1:
                criticos = sp.solve(sp.Eq(res, 0), x)
                st.write("*Candidatos a puntos críticos (f'(x)=0):*", criticos)
                for c in criticos:
                    st.write(f"En x = {c}, f(x) = {sp.simplify(expr.subs(x, c))}")
                st.caption("También pueden existir puntos críticos donde la derivada no existe; revisa el dominio de la función.")
        except Exception as e:
            st.error(f"No se pudo derivar. Detalle: {e}")

# ==================== INTEGRALES ====================
elif modulo == "Integrales":
    st.header("Integrales")
    texto = st.text_input("Integrando f(x)", "3*x^2 + 2*x")
    definida = st.checkbox("Calcular integral definida")
    if definida:
        c1, c2 = st.columns(2)
        a = c1.number_input("Límite inferior", value=0.0)
        b = c2.number_input("Límite superior", value=2.0)
    if st.button("Integrar", type="primary"):
        try:
            expr = parse_expr(texto)
            primitiva = sp.integrate(expr, x)
            st.markdown("*Procedimiento:*")
            st.write("1. Se identifica el integrando.")
            st.write("2. Se aplican reglas de integración; para potencias, se aumenta el exponente en uno y se divide entre el nuevo exponente cuando aplica.")
            st.latex(r"\int " + sp.latex(expr) + r"\,dx = " + sp.latex(primitiva) + " + C")
            if definida:
                res = sp.integrate(expr, (x, a, b))
                st.write(f"3. Se evalúa la primitiva entre {a} y {b}.")
                st.success(f"Integral definida = {res}")
            else:
                st.success(f"Integral indefinida = {primitiva} + C")
        except Exception as e:
            st.error(f"No se pudo integrar. Detalle: {e}")

# ==================== APLICACIONES ====================
elif modulo == "Aplicaciones":
    st.header("Aplicaciones: máximos, mínimos y razones de cambio")
    texto = st.text_input("Función f(x)", "x^3 - 6*x^2 + 9*x + 1")
    if st.button("Analizar puntos críticos", type="primary"):
        try:
            expr = parse_expr(texto)
            primera = sp.diff(expr, x)
            segunda = sp.diff(expr, x, 2)
            candidatos = sp.solve(sp.Eq(primera, 0), x)
            st.write("*1. Primera derivada:*")
            st.latex(sp.latex(primera))
            st.write("*2. Se iguala f'(x) a cero para encontrar candidatos:*", candidatos)
            if not candidatos:
                st.info("No se encontraron soluciones de f'(x)=0. Revisa también puntos donde la derivada no exista.")
            for c in candidatos:
                valor_f = sp.simplify(expr.subs(x, c))
                valor_segunda = sp.simplify(segunda.subs(x, c))
                if valor_segunda.is_positive:
                    tipo = "mínimo relativo (f''(x) > 0)"
                elif valor_segunda.is_negative:
                    tipo = "máximo relativo (f''(x) < 0)"
                else:
                    tipo = "clasificación no concluyente con la segunda derivada"
                st.markdown(f"*En x = {c}:* f(x) = {valor_f}; f''(x) = {valor_segunda}.")
                st.write(f"Clasificación: {tipo}.")
            st.write("*Interpretación:* los puntos críticos ayudan a identificar cambios de crecimiento y posibles máximos o mínimos locales.")
        except Exception as e:
            st.error(f"No se pudo analizar la función. Detalle: {e}")

# ==================== PRÁCTICA ====================
elif modulo == "Práctica con retroalimentación":
    st.header("Práctica con retroalimentación")
    banco = [
        {"pregunta": "¿Cuál es la derivada de x^2?", "respuesta": "2*x", "ayuda": "Usa la regla de la potencia: d(x^n)/dx = n*x^(n-1)."},
        {"pregunta": "Factoriza x^2 - 9.", "respuesta": "(x - 3)*(x + 3)", "ayuda": "Es una diferencia de cuadrados: a^2-b^2=(a-b)(a+b)."},
        {"pregunta": "¿Cuánto vale f(2) si f(x)=x^2+1?", "respuesta": "5", "ayuda": "Sustituye x por 2: 2^2+1."},
        {"pregunta": "¿Cuál es una primitiva de 2*x?", "respuesta": "x^2", "ayuda": "Aumenta el exponente en uno y divide entre el nuevo exponente."},
        {"pregunta": "Resuelve x - 7 = 0. Escribe el valor de x.", "respuesta": "7", "ayuda": "Suma 7 a ambos lados."},
        {"pregunta": "¿Cuál es la derivada de 5*x?", "respuesta": "5", "ayuda": "La derivada de a*x es a."},
        {"pregunta": "Calcula el límite de (x^2-4)/(x-2) cuando x tiende a 2.", "respuesta": "4", "ayuda": "Factoriza x^2-4=(x-2)(x+2) y simplifica."},
        {"pregunta": "Factoriza x^2+5*x+6.", "respuesta": "(x + 2)*(x + 3)", "ayuda": "Busca dos números que sumen 5 y cuyo producto sea 6."},
        {"pregunta": "¿Cuál es la segunda derivada de x^3?", "respuesta": "6*x", "ayuda": "Primero deriva x^3 y luego deriva el resultado."},
        {"pregunta": "¿Cuál es la integral indefinida de 1?", "respuesta": "x", "ayuda": "La derivada de x es 1; recuerda que una integral indefinida incluye + C."}
    ]
    if "practica_actual" not in st.session_state:
        st.session_state.practica_actual = random.choice(banco)
    ejercicio = st.session_state.practica_actual
    st.write(ejercicio["pregunta"])
    respuesta_usuario = st.text_input("Tu respuesta", key="respuesta_practica")
    col_a, col_b = st.columns(2)
    if col_a.button("Comprobar respuesta", type="primary"):
        try:
            correcta = sp.simplify(parse_expr(respuesta_usuario) - parse_expr(ejercicio["respuesta"])) == 0
            if correcta:
                st.success("¡Correcto! Muy buen trabajo.")
            else:
                st.error("Todavía no es correcto. Revisa el procedimiento e intentalo otra vez.")
                st.info("Pista: " + ejercicio["ayuda"])
        except Exception:
            st.error("No se pudo interpretar tu respuesta. Usa x, , ^ o * según corresponda.")
            st.info("Pista: " + ejercicio["ayuda"])
    if col_b.button("Otro ejercicio"):
        st.session_state.practica_actual = random.choice(banco)
        st.session_state.pop("respuesta_practica", None)
        st.rerun()

st.divider()
st.caption("AulaCálculo • Proyecto académico. Personaliza los nombres, asignatura y sección antes de publicar.")