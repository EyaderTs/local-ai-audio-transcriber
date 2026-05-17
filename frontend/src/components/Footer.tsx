import styles from './Footer.module.css';

export function Footer() {
  return (
    <footer className={styles.footer}>
      <p className={styles.text}>Want to build AI apps like this?</p>
      <a
        href="https://github.com/EyaderTs/local-ai-audio-transcriber"
        target="_blank"
        rel="noopener noreferrer"
        className={styles.link}
      >
        Just clone this and learn step by step →
      </a>
    </footer>
  );
}
