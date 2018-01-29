from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_media.protocolentities.message_media_downloadable_image import ImageDownloadableMediaMessageProtocolEntity
import os

class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("success")
    def onSuccess(self, entity):
        self.connected = True
        print("Logged in!", "Auth")
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.jpg')
        self.image_send('79510611033@s.whatsapp.net', image_path)

    @ProtocolEntityCallback("failure")
    def onFailure(self, entity):
        self.connected = False
        print("Login Failed, reason: %s" % entity.getReason())

    def image_send(self, jid, path, caption = None):
        print("requesting upload")
        entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, filePath = path)
        successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, path, successEntity, originalEntity, caption)
        errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)

        self._sendIq(entity, successFn, errorFn)

    def doSendImage(self, filePath, url, to, ip = None, caption = None):
        print("sending image")
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        self.toLower(entity)

    def onRequestUploadResult(self, jid, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, caption = None):
        print("got response from WA")
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            print("is duplicate")
            self.doSendImage(filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
        else:
            print("starting media uploader")
            successFn = lambda filePath, jid, url: self.doSendImage(filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                        resultRequestUploadIqProtocolEntity.getUrl(),
                                        resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                        successFn, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()

    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        print("upload error")
        print(errorRequestUploadIqProtocolEntity)
        # logger.error("Request upload for file %s for %s failed" % (path, jid))

    def onUploadError(self, filePath, jid, url):
        print("upload error")
        # logger.error("Upload file %s to %s for %s failed!" % (filePath, url, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        print("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        pass
  
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        # just print info
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))

