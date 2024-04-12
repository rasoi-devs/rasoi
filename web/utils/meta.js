// generate meta with a default title and description, if none provided
export default function generateMeta(
  title = "Rasoi",
  description = "A social media for recipes 🍳.",
) {
  return {
    metadataBase: new URL(process.env.NEXT_PUBLIC_FRONTEND_URL),
    title: title,
    description: description,
    openGraph: {
      title: title,
      description: description,
      url: process.env.NEXT_PUBLIC_FRONTEND_URL,
      siteName: "Rasoi",
      images: [
        {
          url: "/icon-512-maskable.png",
          width: 512,
          height: 512,
          alt: "Rasoi Logo",
        },
      ],
      locale: "en_US",
      type: "website",
    },
    icons: {
      icon: "/favicon.ico",
      apple: "/apple-touch-icon.png",
    },
    manifest: "/manifest.json",
    // appLinks: {
    //   ios: {
    //     url: 'https://nextjs.org/ios',
    //     app_store_id: 'app_store_id',
    //   },
    //   android: {
    //     package: 'com.example.android/package',
    //     app_name: 'app_name_android',
    //   },
    //   web: {
    //     url: 'https://nextjs.org/web',
    //     should_fallback: true,
    //   },
    // },
  };
}
