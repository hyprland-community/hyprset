from modules.app import MyApplication


def main() -> None:
    try:
        MyApplication.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        exit(0)


if __name__ == '__main__':
    main()
