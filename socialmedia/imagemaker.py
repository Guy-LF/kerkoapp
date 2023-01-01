
#notes. still a lot to do
import text_to_image
encoded_image_path = text_to_image.encode(text, "test.png")

a = platforms.Twitter()
media = a.api.media_upload("test.png")
a.api.update_status(status="hello", media_ids=[media.media_id])  
