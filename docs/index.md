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

<div class="doc-index">
<input id="filtro" type="text" placeholder="Filtrar documentos por nombre...">
<h2>comunidad</h2>
<ul>
  <li data-name="comisiones"><a href="comunidad/comisiones.html">comisiones</a><span class="tipo">html</span></li>
  <li data-name="grupos_de_whatsapp"><a href="comunidad/Grupos_de_WhatsApp.html">Grupos_de_WhatsApp</a><span class="tipo">html</span></li>
  <li data-name="próximas_mejoras"><a href="comunidad/próximas_mejoras.html">próximas_mejoras</a><span class="tipo">html</span></li>
</ul>
<h2>comunidad/Procedimientos</h2>
<ul>
  <li data-name="inclusion_en_grupo_principal_wa"><a href="comunidad/Procedimientos/Inclusion_en_grupo_principal_WA.html">Inclusion_en_grupo_principal_WA</a><span class="tipo">html</span></li>
  <li data-name="reportar_incidentes_de_seguridad"><a href="comunidad/Procedimientos/Reportar_incidentes_de_seguridad.html">Reportar_incidentes_de_seguridad</a><span class="tipo">html</span></li>
</ul>
</div>

<script>
document.getElementById("filtro").addEventListener("input", function (event) {
  var query = event.target.value.toLowerCase();
  document.querySelectorAll("li[data-name]").forEach(function (item) {
    var visible = item.dataset.name.indexOf(query) !== -1;
    item.style.display = visible ? "" : "none";
  });
});
</script>
