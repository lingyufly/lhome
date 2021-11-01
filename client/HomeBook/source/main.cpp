#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

#include "csettings.h"
#include "cajax.h"

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;

    CSettings cSetting("homebook.ini", QSettings::IniFormat);
    engine.rootContext()->setContextProperty("cSetting", &cSetting);

    CAjax cajax;
    cajax.setServerUrl(cSetting.value("server/url").toString());
    cajax.setTimeout(cSetting.value("server/timeout", 3000).toInt());
    engine.rootContext()->setContextProperty("cAjax", &cajax);

    const QUrl url(QStringLiteral("qrc:/qml/main.qml"));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl)
            QCoreApplication::exit(-1);
    }, Qt::QueuedConnection);
    engine.load(url);

    return app.exec();
}
