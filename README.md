# Asistente automatizado para evaluaciones psicológicas

## Autoría

Esta obra es un trabajo realizado por Benearo Semidan Páez Martín como trabajo de fin de grado en ingeniería informática en la ULPGC.

## ¿En qué consiste este asistente?

Como se menciona en el título, el objetivo de este trabajo es facilitar la manera en la que los expertos de la salud mental realizan
evaluaciones psicológicas mediante la automatización del proceso mediante un <i>chatbot</i>.

Actualmente, las preguntas que tiene definidas correponden con el [cuestionario PHQ9](https://www.ons.org/sites/default/files/PatientHealthQuestionnaire9_Spanish.pdf),
 que trata principalmente trastornos del estado de ánimo.

Para ello, se usaron principalmente las siguientes herramientas:

- [Rasa](https://rasa.com/), un framework open source en Python para el desarrollo del agente inteligente.
- Flask, para desarrollar una pequeña aplicación web con Python en la que generar informes de las conversaciones del chatbot.
- [Rasa Webchat](https://github.com/botfront/rasa-webchat), como interfaz gráfica del chatbot, que se presenta a modo de widget.

## ¿Qué se encuentra en este repositorio?

El repositorio contiene tres módulos, cada uno con un propósito concreto.

En primer lugar, tenemos la carpeta [rasa-bot](https://github.com/darkhorrow/chatbot-tfg/tree/master/rasa-bot), la cuál contiene el
trabajo principal. En ella se sitúan los ficheros que conforman el framework de Rasa, además del fichero de la base de datos SQLite
usado para el almacenamiento de las conversaciones.

En segundo lugar, la carpeta [reports-app](https://github.com/darkhorrow/chatbot-tfg/tree/master/demo-page) contiene una pequeña
aplicación en Flask que genera informes a partir de los registros almacenados en la base de datos por Rasa, otorgando dicha información
en un formato más legible.

Finalmente, en [demo-page](https://github.com/darkhorrow/chatbot-tfg/tree/master/demo-page) se encuentra un fichero HTML en blanco 
con el widget [Rasa Webchat](https://github.com/botfront/rasa-webchat) usado para actuar como interfaz gráfica del chatbot.

## ¿Cómo usarlo?

Comenzaremos con la instalación de las dependencias, entrenamiento y ejecución del chatbot.

Para la descarga del repositorio e instalación de las dependencias, usaremos lo siguiente:

    git clone https://github.com/darkhorrow/chatbot-tfg.git
    cd chatbot-tfg/rasa-bot
    pip install -r requirements.txt

Si todo sale bien, ya estaría el proyecto listo para entrenar y posteriormente ejecutar.

Nota: Es importante destacar que durante el desarrollo de este trabajo, Tensorflow no estaba disponible para Python 3.8.x. Si
durante la instalación dicha dependencia resulta ser la conflictiva, compurebe su versión de Python. Si es igual o superior a 3.8,
recomendamos [crear un entorno virtual](https://docs.python.org/3/library/venv.html) con una versión inferior.

El siguiente paso sería entrenar con Rasa Core y Rasa NLU. Para eso, usarmos el siguiente comando:

    rasa train

Posiblemente salgan muchas alertas de Tensorflow si no tienes preparado el equipo para usar la GPU, pero para lo que respecta este trabajo,
no es obligatorio, por lo que podemos ignorarlo.

Una vez realizado el entrenamiento, procederemos a ejecutar el chatbot, usando las siguientes líneas.

    rasa run --cors "*"
    rasa run actions

Estos comandos son bloqueantes, por lo que en general se ejecutarán en consolas distintas. Además, en ocasiones hay que esperar a que el primero acabe para que el segundo pueda ser lanzado sin dar errores.

Con esto, el bot ya está preparado, faltando únicamente la interfaz gráfica.

Si disponemos de un servicio web activo, por ejemplo Apache, bastará con colocar el fichero index.html que está en demo-page en el lugar apropiado.
En distribuciones de Linux, suele ser bajo /var/www/html/.

Sin embargo, si no disponemos de uno, podemos usar el módulo http.server de Python, teniendo en cuenta que el objetivo sea desarrollar/probar y no poner la aplicación en producción.

Este módulo podríamos usarlo así, asumiendo que nos encontramos al igual que cuando terminamos de entrenar el modelo:

    cd ../demo-page
    python -m http.server <puerto>

De esta manera, ya podemos visitar localhost:<puerto> y encontrar ahí un resultado de la siguiente manera:

![BOT](docs/chatbot-enabled.png)

Una vez que tenemos el chatbot listo, podemos habilitar también la aplicación de informes. Partiendo del punto anterior, sería de la siguiente manera:

    cd ../reports-app
    pip install -r requirements.txt
    flask run

Si no hubo problemas en la instalación de las dependencias, esta aplicación debería estar disponible en localhost:5000
