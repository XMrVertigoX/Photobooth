# Maintainer: Caspar Friedrich <c.s.w.friedrich@gmail.com>

pkgname=photobooth
pkgver=0.0.1
pkgrel=1
pkgdesc=
arch=("armv6h")
url=""
license=("MIT")
depends=("python" "python-pip")

install=${pkgname}.install

source=("https://vertigo.canopus.uberspace.de/packages/${pkgname}-${pkgver}.tar.xz")
sha256sums=('e7c41b0a21b1788148a9cc016fec863359d05b6fcd1878e1067323e8aeba2e8c')

build() {
	true
}

package() {
	cd "${srcdir}/${pkgname}-${pkgver}"

	#install "${pkgname}.service" "${pkgdir}/lib/systemd/system/"
	install -D "${pkgname}" "${pkgdir}/opt/${pkgname}"
}
