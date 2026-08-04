---
layout: default
title: Comité de Vecinos de Lomas del Sol
---

# Comité de Vecinos de Lomas del Sol

<p>Punto de referencia para los vecinos de Lomas del Sol, Curridabat.</p>

<p>
Enviá sugerencias y consultas a
<a href="mailto:lomasdelsolcomite@gmail.com">lomasdelsolcomite@gmail.com</a>.
</p>

<p>
<div class="doc-index">
<input id="filtro" type="text" placeholder="Filtrar documentos por nombre...">
<br>
<hr>
<br>
<h2>comite</h2>
<ul>
  <li data-name="estrategia_comisión_salud"><a href="comite/Estrategia_Comisión_Salud.html">Estrategia Comisión Salud</a></li>
  <li data-name="plan_de_trabajo_de_la_comisión_de_integración,_recreación_y_acción_social"><a href="comite/Plan_de_Trabajo_de_la_Comisión_de_Integración,_Recreación_y_Acción_Social.pdf">Plan de Trabajo de la Comisión de Integración, Recreación y Acción Social</a></li>
</ul>
<h2>comunidad</h2>
<ul>
  <li data-name="comisiones"><a href="comunidad/Comisiones.html">Comisiones</a></li>
  <li data-name="grupos_de_whatsapp"><a href="comunidad/Grupos_de_WhatsApp.html">Grupos de WhatsApp</a></li>
  <li data-name="próximas_mejoras"><a href="comunidad/Próximas_mejoras.html">Próximas mejoras</a></li>
</ul>
<h2>comunidad/Procedimientos</h2>
<ul>
  <li data-name="inclusion_en_grupo_principal_wa"><a href="comunidad/Procedimientos/Inclusion_en_grupo_principal_WA.html">Inclusion en grupo principal WA</a></li>
  <li data-name="normas_de_los_grupos_de_vecinos"><a href="comunidad/Procedimientos/Normas_de_los_grupos_de_vecinos.html">Normas de los grupos de vecinos</a></li>
  <li data-name="reportar_incidentes_de_seguridad"><a href="comunidad/Procedimientos/Reportar_incidentes_de_seguridad.html">Reportar incidentes de seguridad</a></li>
</ul>
</div>
</p>

<script>
document.getElementById("filtro").addEventListener("input", function (event) {
  var query = event.target.value.toLowerCase();
  document.querySelectorAll("li[data-name]").forEach(function (item) {
    var visible = item.dataset.name.indexOf(query) !== -1;
    item.style.display = visible ? "" : "none";
  });
});
</script>
