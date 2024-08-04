import { Buffer } from 'buffer'

// Authクラスを返すuseAuthをエクスポートし外部から利用できるようにする
export const useAuth = () => {
  return Auth
}

class Auth {
  // Cookieのキー
  private static ACCESS_TOKEN_KEY: string = "__access_token"
  private static REFRESH_TOKEN_KEY: string = "__refresh_token"

  // 認証済みかどうかの判定
  public static authenticated(type: "access" | "refresh"): boolean {
    let payload = this.getPayload(type)
    if (payload) {
      // トークンの有効期限を検証
      let now  = Math.floor((new Date()).getTime() / 1000)
      return payload.exp > now
    }
    return false
  }

  // CookieからJWTを削除
  public static logout(): void {
    const accessCookie = useCookie(this.ACCESS_TOKEN_KEY)
    const refreshCookie = useCookie(this.REFRESH_TOKEN_KEY)
    accessCookie.value = null
    refreshCookie.value = null
  }

  // JWTをCookieに保存
  public static login(accessToken: string, refreshToken: string): void {
    const accessCookie = useCookie(this.ACCESS_TOKEN_KEY)
    const refreshCookie = useCookie(this.REFRESH_TOKEN_KEY)
    accessCookie.value = accessToken
    refreshCookie.value = refreshToken
  }

  // CookieからJWTを取得する
  public static getToken(type: "access" | "refresh"): string | null {
    const TOKEN_KEY = (type == "access") ? this.ACCESS_TOKEN_KEY : this.REFRESH_TOKEN_KEY
    const cookie = useCookie(TOKEN_KEY);
    let token = cookie.value;
    return (token && Auth.authenticated(type)) ? token : null;
  }

  // Cookieに保存されているJWTのpayloadをオブジェクト形式で取得する
  public static getPayload(type: "access" | "refresh"): any | null {
    const TOKEN_KEY = (type == "access") ? this.ACCESS_TOKEN_KEY : this.REFRESH_TOKEN_KEY
    const cookie = useCookie(TOKEN_KEY)
    let token = cookie.value
    if (!token) return null
    let payload = token.split(".")[1]
    let decoded = Buffer.from(payload, "base64").toString()
    return JSON.parse(decoded)
  }

  // JWTのペイロードからユーザー名を取得する
  public static getUsername(): string | null {
    let payload = Auth.getPayload("access");
    return (payload && !!payload["name"]) ? payload["name"] : null
  }

  // JWTのペイロードからEmailを取得する
  public static getUserEmail(): string | null {
    let payload = Auth.getPayload("access");
    return (payload && !!payload["email"]) ? payload["email"] : null
  }
}