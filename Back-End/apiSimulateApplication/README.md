# cb-dfm-app-sim-back
Backend for the Chilean university application simulator.

# Cuando consultar la API
La API debiese consultarse cuando un alumno del flujo personalizado escoge una carrera universitaria (el flujo general ofrece un solo mensaje para todos los casos, y en caso de escoger una carrera técnico profesional, el mensaje también es fijo). A los estudiantes de colegios sin enseñanza media no se le deben hacer preguntas sobre rendimiento académico o promedio.

# Query Structure
Una consulta a la API debiese tener la siguiente estructura (valores de ejemplo):
```
http://...weighted_careers/?career_id=I70S1C744J2V1&lang=5&math=5&hist=5&scie=0&grade=6.9
```
Donde cada una de las variables significa:
- career_id: El ID de la carrera a consultar (código único)
- lang: Estimación de su rendimiento en el área Lenguaje, valor entre 1 y 10, con un decimal, recogido en las preguntas previas.
- math: Estimación de su rendimiento en el área Matemática, valor entre 1 y 10, con un decimal, recogido en las preguntas previas.
- hist: Estimación de su rendimiento en el área Historia, valor entre 1 y 10, con un decimal, recogido en las preguntas previas.
- scie: Estimación de su rendimiento en el área Sciencia, valor entre 1 y 10, con un decimal, recogido en las preguntas previas.
- grade: Estimación de su promedio final de notas al egresa, valor entre 4 y 7, con un decimal, recogido en las preguntas previas.

En caso de que el estudiante provenga de un colegio sin enseñanza media, el query debiese ser así:
```
http://...weighted_careers/?career_id=I70S1C744J2V1&lang=0&math=0&hist=0&scie=0&grade=0
```

# Salidas
La salida es un diccionario con los siguientes valores:
- application_success: 0 (No, mostrar mensaje correspondiente), 1 (Yes, mostrar mensaje correspondiente), 2 (mostrar mensajes para carreras universitarias con admisión directa), 3 (corresponde a estudiante de colegio sin enseñaza media, no hubo simulación de postulación, no mostrar mensaje).
- biggest_weight: Devuelve 1 o 2 valores entre {Lenguaje y Comunicación, Matemáticas, Historia y Ciencias}.
- ranking_and_nem_over_40: 0 (No, no mostrar mensaje) o 1 (Yes, mostrar mensaje correspondiente).

#Detalle de las Salidas y Mensajes vía Front-End:
Primero, notar que a la API no debiese entrar una consulta para un estudiante que no es del flujo personalizado. Dado que la respuesta para estudiantes del flujo general es una, y la misma para los colegios que no tienen enseñanza media, no es necesario consultar la API y eso se puede gestionar desde el front. El mensaje en ese caso sería:

"Recuerda que las carreras que se imparten en IP o CFT no tienen como requisito rendir la Prueba de Acceso a la Educación Superior (PAES), sin embargo, podrían valorar tus notas de enseñanza media y/o tus aprendizajes previos. Te invitamos a revisar sus requisitos y fechas de admisión en acceso.mineduc.cl"

En cuanto a las consultas válidas, se tienen los siguientes mensajes de salida via front (para el valor "biggest_weight", sólo se sindican posibles ejemplos):
- **{'application success':'1', 'biggest_weight': 'Matemática', 'ranking_and_nem_over_40':'1'}** : "Creemos que vas por buen camino. ¡Sigue así para cumplir tus metas! Te recomendamos prepararte bien para la PAES de Matemática. Además, te contamos que esta carrera valora mucho las notas de enseñanza media, por lo que te recomendamos poner especial atención a tu rendimiento académico."
- **{'application success':'0', 'biggest_weight': 'Lenguaje y Comunicación', 'ranking_and_nem_over_40':'1'}** : "Creemos que debes esforzarte más para alcanzar tus metas. ¡Tú también puedes lograrlo!  Te recomendamos prepararte bien para la PAES de Lenguaje y Comunicación. Además, te contamos que esta carrera valora mucho las notas de enseñanza media, por lo que te recomendamos poner especial atención a tu rendimiento académico."
- **{'application success':'1', 'biggest_weight': 'Matemática, Historia', 'ranking_and_nem_over_40':'0'}** : "Creemos que vas por buen camino. ¡Sigue así para cumplir tus metas! Te recomendamos prepararte bien para la PAES de Matemáticas e Historia."
- **{'application success':'2', 'biggest_weight': '', 'ranking_and_nem_over_40':''}** "Esta carrera no solicita puntaje en la Prueba de Acceso a la Educación Superior (PAES). Te invitamos a revisar sus requisitos y fechas de admisión en acceso.mineduc.cl."

Particularmente, para los colegios que sólo tienen enseñanza básica las respuestas serían:
- **{'application success':'', 'biggest_weight': 'Matemática', 'ranking_and_nem_over_40':'1'}** : "Te recomendamos prepararte bien para la PAES de Matemática. Además, te contamos que esta carrera valora mucho las notas de enseñanza media, por lo que te recomendamos poner especial atención a tu rendimiento académico."
- **{'application success':'', 'biggest_weight': 'Lenguaje y Comunicación, Matemáticas', 'ranking_and_nem_over_40':'0'}** : "Te recomendamos prepararte bien para la PAES de Lenguaje y Comunicación, y Matemátcas."
