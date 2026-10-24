import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import { formatFigureTitle, categorizeFigure, STATIC_FIGURES, FigureItem } from '@/data/figuresList';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export async function GET() {
  try {
    const cwd = process.cwd();
    // Candidate directories where results/figures can reside
    const candidates = [
      path.resolve(cwd, '..', 'results', 'figures'),
      path.resolve(cwd, 'results', 'figures'),
      '/home/jerlin/Documents/projects/blt/results/figures',
      path.resolve(cwd, 'public', 'figures'),
    ];

    const publicFiguresDir = path.resolve(cwd, 'public', 'figures');
    if (!fs.existsSync(publicFiguresDir)) {
      try {
        fs.mkdirSync(publicFiguresDir, { recursive: true });
      } catch (err) {
        // ignore if already exists or permission
      }
    }

    const discoveredFiles = new Set<string>();

    for (const dir of candidates) {
      if (fs.existsSync(dir)) {
        try {
          const files = fs.readdirSync(dir);
          for (const file of files) {
            if (/\.(png|jpe?g|svg|webp)$/i.test(file)) {
              discoveredFiles.add(file);
              // If source directory is not public/figures, sync to public/figures
              if (dir !== publicFiguresDir) {
                const srcPath = path.join(dir, file);
                const destPath = path.join(publicFiguresDir, file);
                try {
                  if (!fs.existsSync(destPath)) {
                    fs.copyFileSync(srcPath, destPath);
                  }
                } catch {
                  // copy attempt non-fatal
                }
              }
            }
          }
        } catch {
          // ignore directory read error
        }
      }
    }

    if (discoveredFiles.size === 0) {
      return NextResponse.json({ figures: STATIC_FIGURES, count: STATIC_FIGURES.length });
    }

    const figures: FigureItem[] = Array.from(discoveredFiles)
      .sort((a, b) => a.localeCompare(b))
      .map((filename) => ({
        filename,
        src: `/figures/${filename}`,
        title: formatFigureTitle(filename),
        category: categorizeFigure(filename),
      }));

    return NextResponse.json(
      { figures, count: figures.length },
      {
        headers: {
          'Cache-Control': 'no-store, max-age=0',
        },
      }
    );
  } catch (error) {
    console.error('Error listing figures:', error);
    return NextResponse.json({ figures: STATIC_FIGURES, count: STATIC_FIGURES.length });
  }
}
