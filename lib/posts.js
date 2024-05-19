import { traverse } from "aubade/compass";

export function getSortedPosts() {
  console.log("Current working directory:", process.cwd());
  const contentPath = process.cwd() + "/content";
  console.log("Accessing content at:", contentPath);
  const posts = traverse(contentPath).hydrate(
    ({ breadcrumb: [filename], buffer, marker, parse }) => {
      const slug = filename.slice(0, -".md".length);
      const { body, metadata } = parse(buffer.toString("utf-8"));

      return {
        ...metadata,
        slug,
        content: marker.render(body),
      };
    },
    (path) => path.endsWith(".md")
  );

  return posts.sort((x, y) => (x.date < y.date ? 1 : -1));
}
