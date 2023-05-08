<template>
  <v-container>
  <br>
  <h4>¿Quieres conocer más información sobre los beneficios estudiantiles que entrega el Estado?
    Haz click sobre cada uno de ellos para indagar más.</h4>
  <br>
  <v-expansion-panels focusable>
    <v-expansion-panel >
      <v-expansion-panel-header><h3>Gratuidad</h3></v-expansion-panel-header>
      <v-expansion-panel-content>
        <br>
        <p>Es un beneficio que está dirigido a las familias correspondientes al 60% de menores ingresos.
        Cubre el 100% del arancel y la matrícula en instituciones adscritas durante la duración
        oficial de la carrera.</p>
        <br>
        <p>¡Una buena parte de las personas que acceden a la educación superior
          estudian con gratuidad, tú también puedes ser uno!</p>
        <br>
      </v-expansion-panel-content>
    </v-expansion-panel>
    <v-expansion-panel >
      <v-expansion-panel-header><h3>Becas</h3></v-expansion-panel-header>
      <v-expansion-panel-content>
        <div v-for="item in benefits" :key="item.ben_id">
          <br><h4>{{ item.ben_name }}</h4>
          <!-- <br><p>{{ item.ben_description }}<b> Requisitos:</b> {{ item.requisite_summary }}</p> -->
        </div>
        <br><br>
        <p><i>Estas becas podrían ajustarse a tu perfil, te invitamos a conocer sus requisitos y todos
          sus detalles en el <a href="https://portal.beneficiosestudiantiles.cl/" target="_blank">Portal 
          de Beneficios Estudiantiles</a></i>.</p>
      </v-expansion-panel-content>
    </v-expansion-panel>
    <v-expansion-panel >
      <v-expansion-panel-header><h3>Créditos</h3></v-expansion-panel-header>
      <v-expansion-panel-content>
        <br>
        <p>Los créditos estudiantiles te ayudan a cubrir parte del gasto asociado a tu carrera.
        Tendrás un plazo para pagarlo de entre 10 y 20 años, con pagos mensuales que comienzan
        a los 18 meses de egresar.</p>
        <br>
        <p>Actualmente existen dos créditos disponibles, el 
        Fondo Solidario de Crédito Universitario y el Crédito con Garantía Estatal.</p>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
  <br><br><br>
  <v-footer color="primary lighten-1" >
      <v-row align="center" justify="center" no-gutters>
        <v-btn color="white" rounded class="my-2" depressed dark>Regresar</v-btn>
      </v-row>
      <v-row align="center" justify="center" no-gutters>
        <v-btn color="white" rounded class="my-2" depressed dark>Continuar</v-btn>
      </v-row>
  </v-footer>
</v-container>
</template>


<script>
export default {
  name: 'App',
  data(){
    return {
      benefits: []
    }
  },

  async created() {
    var response = await fetch('http://127.0.0.1:8000/personalized_benefits/?rut=22200184-6');
    this.benefits = await response.json();
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
   -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale; 
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
