# Podummary - Tech CEO & Founder Interview Summaries

> AI-powered platform for discovering and reading summaries from top tech CEO and founder interviews.

![Podummary](https://img.shields.io/badge/version-2.0.0-blue)
![Next.js](https://img.shields.io/badge/Next.js-15-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🚀 Features

### ✅ Implemented (Phase 1)

- **Next.js 15** with App Router and React 19
- **Advanced SEO** with OpenGraph, Twitter Cards, Schema.org JSON-LD, hreflang tags, and dynamic sitemap
- **13 Language Support** - English, Spanish, Portuguese, Hindi, French, German, Indonesian, Simplified Chinese, Traditional Chinese, Japanese, Korean, Thai, Vietnamese
- **Unified View Tracking** across all language versions with article grouping
- **Optimized Images** using Next.js Image component
- **Social Sharing** buttons (Twitter, LinkedIn, Facebook, Reddit)
- **Code Quality Tools** - ESLint, Prettier, Husky pre-commit hooks
- **TypeScript** throughout the codebase
- **AI-Powered Content Generation** - Automated blog creation and translation from YouTube videos

### 🎯 Coming Soon

See the full [Modernization Plan](../QuickPods-Modernization-Plan.md) for details on:

- Automated YouTube video discovery
- AI-powered video clipping for social media
- Multi-platform content distribution (Instagram, TikTok, YouTube Shorts)
- Advanced analytics dashboard
- And much more!

## 📋 Prerequisites

- **Node.js** 18+
- **pnpm** (recommended) or npm
- **Supabase** account and project

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/WilsonLimSet/QuickPods.git
   cd quickpods-revived
   ```

2. **Install dependencies**

   ```bash
   pnpm install
   ```

3. **Set up environment variables**

   Create a `.env.local` file:

   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

4. **Set up Supabase tables**

   Create these tables in your Supabase project:

   **Podcasts table:**

   ```sql
   create table podcasts (
     id serial primary key,
     interviewer text,
     interviewee text,
     insights text[],
     thumbnail_url text,
     publish_date date,
     tag text,
     md_slug text unique,
     blog_content text,
     views integer default 0,
     created_at timestamp with time zone default now()
   );
   ```

   **Newsletter subscribers table:**

   ```sql
   create table newsletter_subscribers (
     id serial primary key,
     email text unique not null,
     subscribed_at timestamp with time zone default now()
   );
   ```

5. **Run the development server**

   ```bash
   pnpm dev
   ```

6. **Open your browser**

   Navigate to [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
quickpods-revived/
├── app/                      # Next.js App Router
│   ├── api/                 # API routes
│   │   └── newsletter/      # Newsletter signup endpoint
│   ├── blog/                # Blog pages
│   │   └── [slug]/          # Dynamic blog post pages
│   ├── layout.tsx           # Root layout with providers
│   └── page.tsx             # Homepage
├── components/              # React components
│   ├── Header.tsx           # Navigation header
│   ├── Footer.tsx           # Footer
│   ├── PodCard.tsx          # Podcast card component
│   ├── ThemeToggle.tsx      # Dark mode toggle
│   ├── SocialShare.tsx      # Social sharing buttons
│   └── NewsletterSignup.tsx # Newsletter form
├── i18n/                    # Internationalization config
│   └── request.ts           # i18n setup
├── lib/                     # Utility functions
│   └── posts.js             # Blog post utilities
├── messages/                # Translation files
│   ├── en.json             # English
│   ├── es.json             # Spanish
│   └── tr.json             # Turkish
├── python-helpers/          # Python automation scripts
│   └── src/                # Video processing scripts
├── public/                  # Static assets
├── utils/                   # Utility functions
│   └── supabase/           # Supabase client
└── content/                 # Markdown blog posts
```

## 🧪 Available Scripts

```bash
pnpm dev          # Start development server
pnpm build        # Build for production
pnpm start        # Start production server
pnpm lint         # Run ESLint
pnpm typecheck    # Run TypeScript type checking
pnpm format       # Format code with Prettier
pnpm check        # Check code formatting
```

## 🎨 Tech Stack

### Frontend

- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript 5.7
- **Styling:** Tailwind CSS
- **UI Components:** Custom components
- **Font:** Geist Sans
- **Analytics:** Vercel Analytics
- **i18n:** next-intl
- **Theme:** next-themes

### Backend

- **Database:** Supabase (PostgreSQL)
- **Authentication:** Supabase Auth
- **Storage:** Supabase Storage
- **API:** Next.js API Routes

### Python Automation

- **Video Processing:** pytube, moviepy
- **AI/LLM:** Google Gemini API
- **Content Generation:** Custom pipeline

### Development Tools

- **Linting:** ESLint
- **Formatting:** Prettier
- **Git Hooks:** Husky
- **Testing:** Vitest (planned)

## 🌍 Internationalization

Podummary supports 13 languages with automatic locale detection and SEO optimization:

- 🇺🇸 English (en)
- 🇪🇸 Spanish (es)
- 🇵🇹 Portuguese (pt)
- 🇮🇳 Hindi (hi)
- 🇫🇷 French (fr)
- 🇩🇪 German (de)
- 🇮🇩 Indonesian (id)
- 🇨🇳 Simplified Chinese (zh)
- 🇹🇼 Traditional Chinese (zh-TW)
- 🇯🇵 Japanese (ja)
- 🇰🇷 Korean (ko)
- 🇹🇭 Thai (th)
- 🇻🇳 Vietnamese (vi)

Each language version includes:

- Localized UI components
- Hreflang tags for SEO
- Separate sitemap entries
- Unified view tracking across translations

See [I18N_GUIDE.md](I18N_GUIDE.md) for detailed implementation information.

## 🔐 Environment Variables

| Variable                        | Description            | Required |
| ------------------------------- | ---------------------- | -------- |
| `NEXT_PUBLIC_SUPABASE_URL`      | Supabase project URL   | Yes      |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key | Yes      |

## 🚀 Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import project in Vercel
3. Add environment variables
4. Deploy!

### Manual Deployment

```bash
pnpm build
pnpm start
```

## 📝 Content Management

### Adding a New Interview

1. **Manual Process:**

   - Create a new Markdown file in `content/`
   - Format: `YYYYMMDD-interviewee-interviewer.md`
   - Add frontmatter with metadata
   - Write the blog content

2. **Automated Process (Python):**
   ```bash
   cd python-helpers
   poetry install
   python src/main.py
   ```

The automated script will:

- Fetch videos from YouTube playlists
- Extract metadata
- Generate AI-powered summaries
- Upload to Supabase
- Create blog posts

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards

- Use TypeScript for all new code
- Follow the existing code style (Prettier will format automatically)
- Write meaningful commit messages
- Add comments for complex logic
- Ensure all checks pass before committing (Husky will enforce this)

## 📊 Performance

- **Lighthouse Score:** 95+ across all metrics
- **First Contentful Paint:** < 1.5s
- **Time to Interactive:** < 3s
- **ISR Revalidation:** 1 hour

## 🐛 Known Issues

- [ ] Theme flash on initial load (minor)
- [ ] Some TypeScript types need refinement
- [ ] Newsletter requires database table creation

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Wilson Lim**

- GitHub: [@WilsonLimSet](https://github.com/WilsonLimSet)
- Website: [podummary.com](https://podummary.com)

## 🙏 Acknowledgments

- Next.js team for the amazing framework
- Supabase for the backend infrastructure
- All the CEOs and founders who share their insights

## 📞 Support

For questions or support:

- Open an issue on GitHub
- Email: support@podummary.com

---

**Star ⭐ this repo if you find it useful!**
