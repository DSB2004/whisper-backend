
from celery import shared_task
from .models import User
from django.utils.timezone import now
from datetime import timedelta
import logging
from services.storage import Storage
logger = logging.getLogger('whisper')

class BanCheck:
    @shared_task
    def removeExpiredBan():
        try:
            cutoff_date = now() - timedelta(days=30)
            users_to_unban = User.objects.filter(isBanned=True, bannedAt__lt=cutoff_date)

            for user in users_to_unban:
                user.isBanned = False
                user.bannedAt = None
                user.save()
            
            logger.info(f"[REMOVE_EXPIRED_BAN] Unbanned {users_to_unban.count()} user(s) who were banned over 30 days ago.")
        except Exception as e:
            logger.error(f"[REMOVE_EXPIRED_BAN] Failed to unban user {e}")

class UpdateProfilePic:
    @shared_task
    def updateProfilePic(email,file):
 
        try:
            user=User.objects.get(email=email)
            url=user.profilePic
            if(url is not None):
                try:
                    Storage.deleteFile(url)
                except Exception :
                    logger.warning(f"[UPDATE_USER_PROFILE_PIC] Unable to delete old profile pic")
                
            url=Storage.uploadFile(file)
            user.profilePic=url
            user.save()
 
        except User.DoesNotExist:
            logger.error(f"[UPDATE_USER_PROFILE_PIC] User not found")
            pass
        except Exception as e:
            logger.error(f"[REMOVE_EXPIRED_BAN] Failed to unban user {e}")
    

   
CRON_JOBS = [
    {
        "name": "Remove expired bans",
        "task": "user.tasks.removeExpiredBan",
        "schedule": {"minute": "0", "hour": "0", "day_of_week": "*", "day_of_month": "*", "month_of_year": "*"},
        "args": [],
        "kwargs": {}
    }
]
