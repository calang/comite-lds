# Dominio propio, DNS y migración futura a OCI para el sitio en GitHub Pages
Creado el 2026-08-06

## Pregunta

me interesa obtener un nombre de dominio propio para el sitio que ahora desplegamos en github pages. He leído de varias opciones, como dominios.cr, para dominios como lomasdelsol.or.cr, o Cloudflare, Porkbun, para dominios como lomasdelsol.org. Además, necesito de algún servicio de DNS; ¿github lo provee? Si no, donde lo puedo obtener para no tener que crear mi propia instancia física? ¿cuál es la forma más sencilla de obtener el servicio DNS y de configurarlo? cuando pase el despliegue del sitio a OCI, ¿qué tan fácil será trasladar el dominio para que mapee a ese sitio?

## Respuesta

### Dominio

- **`.or.cr`** (vía `dominios.cr`, que es el sitio propio de NIC Costa Rica): los TLD sectoriales como `.or.cr` piden documentación del sector (para una organización comunitaria, típicamente personería jurídica o equivalente). No hay restricción de residencia para registrar, pero sí trámite documental.
- **`.org`** (vía Porkbun o Cloudflare Registrar): registro internacional, sin papeleo local, ~US$10-15/año, todo por tarjeta en minutos.

Si querés evitar trámites, `lomasdelsol.org` es la ruta simple. Si te importa la identidad "Costa Rica" en el dominio, `.or.cr` es válido pero implica reunir la documentación que pida NIC.cr.

### DNS

GitHub **no** ofrece DNS — solo te dice qué registros crear. Necesitás un proveedor de DNS aparte.

**Opción más simple: Cloudflare (plan gratuito)**, funciona sin importar dónde compres el dominio (Porkbun, Cloudflare Registrar, o incluso `dominios.cr`, que admite nameservers externos — mínimo 2, máximo 9). El proceso es:
1. Creás cuenta gratis en Cloudflare, agregás tu dominio.
2. Cloudflare te da 2 nameservers propios.
3. Cambiás los nameservers del dominio en el registrar (Porkbun/dominios.cr) para que apunten a esos 2.
4. En Cloudflare creás los registros que pide GitHub Pages:
   - Apex (`lomasdelsol.org`): 4 registros **A** a `185.199.108.153`, `.109.153`, `.110.153`, `.111.153`.
   - `www`: registro **CNAME** a `calang.github.io` (tu subdominio de GitHub Pages).
5. En el repo, `Settings → Pages → Custom domain` con el dominio elegido (esto genera el archivo `CNAME` en `docs/`).

### Migración futura a OCI

Con este esquema (Cloudflare como DNS, separado del registrar y del hosting), el traslado es trivial: **solo cambiás los registros A/CNAME** en Cloudflare para que apunten a la IP o load balancer de OCI en vez de a las IPs de GitHub Pages. El dominio no se mueve de registrar ni de DNS — nada que transferir, solo editar registros y esperar la propagación (minutos a pocas horas). Esta es justamente la ventaja de no dejar el DNS "adentro" del registrar: desacopla dominio, DNS y hosting, así que el día que decidas migrar es un cambio de 5 minutos, no una migración de dominio.

**Recomendación**: `lomasdelsol.org` vía Porkbun (o Cloudflare Registrar) + Cloudflare DNS gratuito. Evitás el trámite documental de `.or.cr` y quedás listo para mover a OCI sin fricción.

Sources:
- [faqs | NIC Costa Rica](https://dominios.cr/faqs)
- [Capítulo 1: Registro de un Nombre de Dominio - NIC Costa Rica](https://nic.cr/capitulo-1-registro-de-un-nombre-de-dominio/)
- [Free Plan Overview | Cloudflare](https://www.cloudflare.com/plans/free/)
- [About custom domains and GitHub Pages - GitHub Docs](https://docs.github.com/articles/about-supported-custom-domains)
- [Managing a custom domain for your GitHub Pages site - GitHub Docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)

---

## Pregunta (seguimiento)

Si creo el dominio en CloudFlare, ¿porqué habría de realizar el paso 3 en Porkbun/dominios.cr? O ¿entendí más ese paso? ¿Puedes explicar ese paso en un poco detalle?

## Respuesta (seguimiento)

Tenés razón en dudarlo — depende de dónde compres el dominio:

- **Si lo comprás en Cloudflare Registrar** (solo disponible para `.org`, no para `.or.cr` — Cloudflare Registrar no vende ccTLDs como `.cr`): el dominio ya nace con los nameservers de Cloudflare asignados. **No hay paso 3**, vas directo a crear los registros DNS.
- **Si lo comprás en Porkbun o en `dominios.cr`** (obligatorio para `.or.cr`, ya que Cloudflare no lo ofrece): el registrar te asigna sus propios nameservers por defecto (ej. `curitiba.ns.porkbun.com` o los de NIC.cr). Cloudflare no puede gestionar el DNS de tu dominio hasta que le "cedas" esa función — ahí entra el paso 3.

### Qué es el paso 3 en detalle

Un dominio tiene un registro de **delegación NS** en el registro central (el WHOIS): le dice a internet "para resolver este dominio, preguntale a estos servidores de nombres". Ese registro es independiente de quién es el dueño/registrante — es configurable desde el panel del registrar.

Pasos concretos:
1. En Cloudflare, al agregar el dominio, te muestra dos nameservers propios, algo como:
   ```
   ana.ns.cloudflare.com
   bob.ns.cloudflare.com
   ```
2. Entrás al panel de Porkbun (o dominios.cr) → la sección del dominio → **"Nameservers"** o **"DNS"**.
3. Reemplazás los nameservers que trae por defecto por esos dos de Cloudflare.
4. Guardás. La propagación toma de minutos a ~24h (normalmente rápido).
5. Cloudflare detecta el cambio automáticamente y activa la zona; desde ahí toda la gestión de registros (A, CNAME, etc.) se hace en Cloudflare, aunque el dominio siga "comprado" en Porkbun/dominios.cr.

Es decir: el **registrar** (dueño del contrato de la marca del dominio) y el **proveedor DNS** (quién resuelve las consultas) son roles separados, y el paso 3 es lo que conecta uno con el otro cuando no coinciden.

**Para tu caso**: como `.or.cr` obliga a comprar en `dominios.cr`, el paso 3 es inevitable ahí. Si en cambio vas por `.org`, podés simplificarte la vida comprándolo directo en Cloudflare Registrar y saltarte ese paso.
