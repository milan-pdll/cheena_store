// Core TypeScript type definitions matching backend database and API models

export type CategorySlug = "boots" | "jerseys" | "accessories";

export type GroundType = "FG" | "AG" | "SG" | "TF" | "IC";

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  is_active: boolean;
}

export interface Brand {
  id: number;
  name: string;
  slug: string;
  logo_url?: string;
  is_active: boolean;
}

export interface ProductImage {
  id: number;
  product_id: number;
  url: string;
  public_id?: string;
  position: number;
  is_primary: boolean;
}

export interface ProductVariant {
  id: number;
  product_id: number;
  size: string;
  color: string;
  stock_quantity: number;
  sku: string;
  ground_type?: GroundType | null;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  category: Category;
  brand: Brand;
  price: number;
  discount_price?: number | null;
  currency: string;
  is_active: boolean;
  is_featured: boolean;
  featured_order: number;
  images: ProductImage[];
  variants: ProductVariant[];
  created_at: string;
  updated_at: string;
}

export interface SiteSettings {
  store_name: string;
  whatsapp_number: string;
  instagram_url?: string;
  facebook_url?: string;
  hero_title: string;
  hero_subtitle: string;
  contact_email?: string;
  address?: string;
}
