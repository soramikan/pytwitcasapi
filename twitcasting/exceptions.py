class TwitCastingInvailedTokenException(Exception):
    """Exception raised for invalid token errors."""
    pass

class TwitCastingValidationErrorException(Exception):
    """Exception raised for validation errors."""
    pass

class TwitCastingInvalidWebhookURLException(Exception):
    """Exception raised for invalid webhook URL errors."""
    pass

class TwitCastingExecutionCountLimitationException(Exception):
    """Exception raised for execution count limitation errors."""
    pass

class TwitCastingApplicationDisabledException(Exception):
    """Exception raised for disabled application errors."""
    pass

class TwitCastingProtectedException(Exception):
    """Exception raised for protected content errors."""
    pass

class TwitCastingDuplicateException(Exception):
    """Exception raised for duplicate comments errors."""
    pass

class TwitCastingTooManyCommentsException(Exception):
    """Exception raised for too many comments errors."""
    pass

class TwitCastingOutOfScopeException(Exception):
    """Exception raised for out of scope errors."""
    pass

class TwitCastingEmailUnverifiedException(Exception):
    """Exception raised for unverified email errors."""
    pass

class TwitCastingBadRequestException(Exception):
    """Exception raised for bad request errors."""
    pass

class TwitCastingForbiddenException(Exception):
    """Exception raised for forbidden errors."""
    pass

class TwitCastingNotFoundException(Exception):
    """Exception raised for not found errors."""
    pass

class TwitCastingInternalServerErrorException(Exception):
    """Exception raised for internal server errors."""
    pass

ERROR_CODES_DICT = {
    1000: ("Invalid Token", "アクセストークンが不正", TwitCastingInvailedTokenException),
    1001: ("Validation Error", "バリデーションエラー", TwitCastingValidationErrorException),
    1002: ("Invalid Webhook URL", "WebHook URL の登録が必要なAPIで、URLが登録されていない または URLの形式が不正", TwitCastingInvalidWebhookURLException),
    2000: ("Execution Count Limitation", "APIの実行回数上限", TwitCastingExecutionCountLimitationException),
    2001: ("Application Disabled", "アプリケーションが無効化されてます（サポートへお問い合わせください）", TwitCastingApplicationDisabledException),
    2002: ("Protected", "コンテンツが保護されている (合言葉配信等)", TwitCastingProtectedException),
    2003: ("Duplicate Comment", "多重投稿時 (連続で同じコメントを送信した時等)", TwitCastingDuplicateException),
    2004: ("Too Many Comments", "コメント数が上限に達している (一定数以上のコメントがある配信で、配信が終了している場合にこのエラーが発生することがあります)", TwitCastingTooManyCommentsException),
    2005: ("Out of Scope", "書込み・配信などの権限がない", TwitCastingOutOfScopeException),
    2006: ("Email Unverified", "Emailの確認が済んでおらず機能が利用できない", TwitCastingEmailUnverifiedException),
    400: ("Bad Request", "パラメータが不正な時 (バリデーション上問題ないが、パラメータで指定した対象が存在しない場合等)", TwitCastingBadRequestException),
    403: ("Forbidden", "権限の無いリソースへのアクセス", TwitCastingForbiddenException),
    404: ("Not Found", "コンテンツが見つからない", TwitCastingNotFoundException),
    500: ("Internal Server Error", "その他エラー", TwitCastingInternalServerErrorException),
}
