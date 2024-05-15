import { traverse } from "aubade/compass";

export function getSortedPosts() {
  const posts = traverse(process.cwd() + "/content").hydrate(
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
