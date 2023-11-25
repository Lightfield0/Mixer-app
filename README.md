# Volume Mixer

## Genel Bakış
Bu proje, Windows işletim sistemi için bir ses karıştırıcı uygulamasıdır. PyQt6 ve pycaw kütüphanelerini kullanarak geliştirilmiştir. Uygulama, kullanıcının sistemdeki tüm ses oturumlarının ses seviyelerini ayarlamasına olanak tanır.

## Özellikler
- Sistemdeki tüm ses oturumlarını görüntüleme.
- Her bir ses oturumu için ses seviyesini ayarlama.
- Ses oturumlarını sessize alma.
- Otomatik yenileme özelliği ile yeni açılan uygulamaları algılama.

## Kurulum
Projeyi çalıştırmak için aşağıdaki adımları izleyin:

1. Python'ın son sürümünü yükleyin.
2. Bu repoyu klonlayın veya indirin.
3. Terminal veya komut istemcisinde, projenin bulunduğu dizine gidin.
4. Gerekli kütüphaneleri yüklemek için `pip install -r requirements.txt` komutunu çalıştırın.
5. Uygulamayı başlatmak için `python main.py` komutunu çalıştırın.

## Gereksinimler
- Python 3.9 veya üstü
- PyQt6
- pycaw
- qdarktheme

## Kullanım
Uygulamayı başlattığınızda, sistemdeki tüm ses oturumlarını bir liste halinde göreceksiniz. Her bir oturum için aşağıdaki işlemleri yapabilirsiniz:

- Ses seviyesini ayarlamak için kaydırıcıyı kullanın.
- Sessize almak için mute butonuna basın.
- Yeni açılan uygulamalar otomatik olarak listeye eklenecektir.

