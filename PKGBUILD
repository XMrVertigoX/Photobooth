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
sha256sums=('b499eab34a5c5fa12b74a31606caa30dbfa8db2d354e28a1718df83cd20d7e22')

build() {
	true
}

package() {
	cd "${srcdir}/${pkgname}-${pkgver}"

	#install -D "${pkgname}/${pkgname}.service" "${pkgdir}/lib/systemd/system/"
	install -D "${pkgname}" "${pkgdir}/opt/${pkgname}"
}
