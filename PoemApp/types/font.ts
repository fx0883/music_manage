export interface Font {
  code: string
  name: string
  file_url: string
  preview_url: string
  is_active: boolean
}

export interface FontCategory {
  code: string
  name: string
  description: string
  order: number
  fonts: Font[]
}

export interface FontFaceDescriptors {
  family: string
  style?: string
  weight?: string
  stretch?: string
  unicodeRange?: string
  variant?: string
  featureSettings?: string
  display?: string
}

export interface FontFace {
  family: string
  style: string
  weight: string
  stretch: string
  unicodeRange: string
  variant: string
  featureSettings: string
  status: string
  load(): Promise<FontFace>
  loaded: Promise<FontFace>
}

export type FontLoadStatus = 'unloaded' | 'loading' | 'loaded' | 'error'

export interface FontLoadEvent extends Event {
  readonly fontfaces: FontFace[]
} 