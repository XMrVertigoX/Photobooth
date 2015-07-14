# Maintainer: Caspar Friedrich <c.s.w.friedrich@gmail.com>

pkgname=photobooth
pkgver=0.0.1
pkgrel=1
pkgdesc=
arch=("armv6h")
url=""
license=("MIT")
depends=("base-devel" "lirc" "python" "python-pip" "gphoto2" "terminus-font")

install=${pkgname}.install

source=("https://vertigo.canopus.uberspace.de/packages/${pkgname}-${pkgver}.tar.xz")
sha256sums=('1bb666d9c574933770bc29dfef7bf953772775af9b2ce19c195b19a77e81250c')

build() {
	true
}

package() {
	cd "${srcdir}/${pkgname}-${pkgver}"

	#install -D "${pkgname}/${pkgname}.service" "${pkgdir}/lib/systemd/system/"
	install -D "${pkgname}" "${pkgdir}/opt/${pkgname}"
}
